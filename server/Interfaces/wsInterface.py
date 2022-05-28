#!/bin/python3

import asyncio
import websockets
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

group = 'websocket'


class AccessNode:  #Implementierungs unterschiede

    def __init__(self, name, wideAccess, websocket, path):
        self.name = name
        self.isWideAccess = wideAccess
        self.websocket = websocket
        self.path = path

    async def send(self, data):  #Implementierungs unterschiede
        await self.websocket.send(data.decode())

    async def handel(self):  #Implementierungs unterschiede
        try:
            async for message in self.websocket:
                await writeStream(self.name, message[:message.find('@')], message[message.find('@')+1:message.find(':')], message[message.find(':')+1:])

        except: pass
        finally:
            if self.isWideAccess: wideAccessNodes.remove(self)
            else: narrowAccessNodes.pop(self.name)


async def readStream():  # origin@origingroup>target@targetgroup:message\n
    return (await reader.readuntil(b'>')).decode()[:-1], (await reader.readuntil(b'@')).decode()[:-1], (await reader.readuntil(b':')).decode()[:-1], (await reader.readuntil(b'\n')).decode()[:-1]


async def listenStream():
    try:
        while not reader.at_eof():
            origin, target, targetgroup, message = await readStream()
            if targetgroup == group and target in narrowAccessNodes: await narrowAccessNodes[target].send(message.encode())
            data = f"{origin}>{target}@{targetgroup}:{message}\n".encode()
            for accessNode in wideAccessNodes: await accessNode.send(data)
    except: pass
    finally:
        pass


async def writeStream(origin, target, targetgroup, message):
    writer.write(f"{origin}>{target}@{targetgroup}:{message}\n".encode())
    await writer.drain()


async def accessPoint():  #Implementierungs unterschiede
    await websockets.serve(accessSetup, "0.0.0.0", 5678)


async def accessSetup(websocket, path):
    setup = (await websocket.recv()).split(':')
    if setup[1] == 'w':
        wideAccessNodes.append(AccessNode(setup[0], True, websocket, path))
        await wideAccessNodes[-1].handel()
    else:
        narrowAccessNodes[setup[0]] = AccessNode(setup[0], False, websocket, path)
        await narrowAccessNodes[setup[0]].handel()


async def main():
    global reader, writer
    reader, writer = await asyncio.open_unix_connection(PATH)
    writer.write(group.encode()+b'\n')
    await writer.drain()
    await asyncio.gather(listenStream(), accessPoint())


asyncio.run(main())
