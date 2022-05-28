import asyncio
import serial
import serial.tools.list_ports

global reader, writer
narrowAccessNodes = dict()
wideAccessNodes = []

group = 'serial'

BAUDRATE = 9600

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
        await self.sendQueue.put(data)

    def handel(self):  #Implementierungs unterschiede
        try:
            messageAvailable = self.serial.read(1)
            if self.sendQueue.qsize() > 0:
                self.serial.write(b'y')
                self.serial.write(self.sendQueue.get_nowait())
            else: self.serial.write(b'n')
            if messageAvailable == b'y': self.recvQueue.put_nowait(self.serial.readline().decode()[:-1])
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
        if 'ACM' in i.device: accessSetup(i.device, loop)


def accessSetup(dev, loop):
    serial_f = serial.Serial(port=dev, baudrate=BAUDRATE)

    serial_f.write(b't')
    setup = serial_f.readline().decode()[:-1].split(':')

    print(setup)
    if setup[1] == 'w':
        wideAccessNodes.append(AccessNode(setup[0], True, serial_f, loop))
        loop.add_reader(serial_f, wideAccessNodes[-1].handel)
    else:
        narrowAccessNodes[setup[0]] = AccessNode(setup[0], False, serial_f, loop)
        loop.add_reader(serial_f, narrowAccessNodes[setup[0]].handel)



async def main():
    global reader, writer
    reader, writer = await asyncio.open_unix_connection('../DistributionStream.sock')
    writer.write(group.encode()+b'\n')
    await writer.drain()
    await asyncio.gather(listenStream(), accessPoint())


asyncio.run(main())
