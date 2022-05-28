#!/bin/python3

import asyncio
import serial
import serial.tools.list_ports
from asyncinotify import Inotify, Mask
import sys

if len(sys.argv) < 2:
        print(sys.argv[0]+" <Path where to put Unix Socked>", file=sys.stderr)
        exit(1)

PATH = sys.argv[1]
if PATH[-1] != "/": 
    PATH += "/"
PATH += "DistributionStream.sock"

global reader, writer
narrowAccessNodes = dict()
wideAccessNodes = []

group = 'serial'

BAUDRATE = 9600
SELECTORS = ['ACM']

class AccessNode:  #Implementierungs unterschiede

    def __init__(self, name, wideAccess, serialv, loop):
        self.name = name
        self.isWideAccess = wideAccess
        self.serial = serialv
        self.loop = loop
        self.sendQueue = asyncio.Queue()
        self.recvQueue = asyncio.Queue()
        self.device = self.serial.fileno()
        self.open = True

        loop.create_task(self.talker())

    async def send(self, data):  #Implementierungs unterschiede
        self.serial.write(data)
        #await self.sendQueue.put(data)

    def handel(self):  #Implementierungs unterschiede
        try:
            self.recvQueue.put_nowait(self.serial.readline().decode()[:-1])
        except Exception as e:
            print(e)
            try: self.loop.remove_reader(self.serial)
            except: pass
            try: self.serial.close()
            except: pass
            if self.isWideAccess: wideAccessNodes.remove(self)
            else: narrowAccessNodes.pop(self.name)
            self.open = False
        finally: pass

    async def talker(self):
        while self.open:
            message = await self.recvQueue.get()
            await writeStream(self.name, message[:message.find('@')], message[message.find('@') + 1:message.find(':')], message[message.find(':') + 1:])


async def readStream():  # origin@origingroup>target@targetgroup:message\n
    return (await reader.readuntil(b'>')).decode()[:-1], (await reader.readuntil(b'@')).decode()[:-1], (await reader.readuntil(b':')).decode()[:-1], (await reader.readuntil(b'\n')).decode()[:-1]


async def listenStream():
    try:
        while not reader.at_eof():
            origin, target, targetgroup, message = await readStream()
            if targetgroup == group and target in narrowAccessNodes: await narrowAccessNodes[target].send(f'{message}\n'.encode())
            data = f"{origin}>{target}@{targetgroup}:{message}\n".encode()
            for accessNode in wideAccessNodes: await accessNode.send(data)
    except: pass
    finally:
        pass


async def writeStream(origin, target, targetgroup, message):
    writer.write(f"{origin}>{target}@{targetgroup}:{message}\n".encode())
    await writer.drain()


async def accessPoint():  #Implementierungs unterschiede
    loop = asyncio.get_event_loop()

    for i in serial.tools.list_ports.comports():
        print(i)
        await tryRegister(i.device, loop)
        #if 'ACM' in i.device: accessSetup(i.device, loop)

    with Inotify() as inotify:
        inotify.add_watch('/dev/', Mask.CREATE)
        async for event in inotify:
            print("Found new dev:",event.path.as_posix())
            await asyncio.sleep(0.5)
            await tryRegister(event.path.as_posix(),loop)


async def tryRegister(path,loop):
    if "tty" in path:
        for selector in SELECTORS:
            if selector in path:
                accessSetup(path,loop)


#def doSetup(device):
#    pass

def accessSetup(dev, loop):
    print(dev)
    serial_f = serial.Serial(port=dev, baudrate=BAUDRATE)

    serial_f.read(6)
    serial_f.write(b'hello\n')
    setup = serial_f.readline().decode()[:-1].split(':')

    if setup[1] == 'w':
        print("wideAccessNodes with name:",setup[0])
        wideAccessNodes.append(AccessNode(setup[0], True, serial_f, loop))
        loop.add_reader(serial_f, wideAccessNodes[-1].handel)
    else:
        print("narrowAccessNodes with name:",setup[0])
        narrowAccessNodes[setup[0]] = AccessNode(setup[0], False, serial_f, loop)
        loop.add_reader(serial_f, narrowAccessNodes[setup[0]].handel)



async def main():
    global reader, writer
    reader, writer = await asyncio.open_unix_connection(PATH)
    writer.write(group.encode()+b'\n')
    await writer.drain()
    await asyncio.gather(listenStream(), accessPoint())


asyncio.run(main())
