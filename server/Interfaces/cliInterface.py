#!/bin/python3

import asyncio
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

group = 'cli'


class AccessNode:  #Implementierungs unterschiede
    def __init__(self, name, wideAccess,queue):
        self.name = name
        self.isWideAccess = wideAccess
        self.queue = queue

    def _stdin_data(self):
        self.queue.put_nowait(sys.stdin.readline())

    async def send(self, data):  #Implementierungs unterschiede
        print(data.decode(), end="")

    async def handel(self):  #Implementierungs unterschiede
        asyncio.get_event_loop().add_reader(sys.stdin, self._stdin_data)
        print("target\ntargetgroup\nmessage\n-----------------")
        try:
            while True:
                target = (await self.queue.get())[:-1]
                targetgroup = (await self.queue.get())[:-1]
                message = (await self.queue.get())[:-1]
                print("-----------------")
                await writeStream(self.name, target, targetgroup, message)
        except: pass
        finally:
            writer.close() # Nicht bei anderen machen (also nur bei cli)


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
    wideAccessNodes.append(AccessNode('cli', True,asyncio.Queue()))
    await wideAccessNodes[-1].handel()


async def main():
    global reader, writer
    reader, writer = await asyncio.open_unix_connection(PATH)
    writer.write(group.encode()+b'\n')
    await writer.drain()
    await asyncio.gather(listenStream(), accessPoint())


asyncio.run(main())
