#!/bin/python3

# Importiert das asyncio Modul
import asyncio
import sys

if len(sys.argv) < 2:
	print(sys.argv[0]+" <Path where to put Unix Socked>", file=sys.stderr)
	exit(1)

PATH = sys.argv[1]
if PATH[-1] != "/":
    PATH += "/"
PATH += "DistributionStream.sock"

# Liste aller eingehängten Interfaces
interfaces = dict()


# Sendet message von einem Interface zu allen anderen
def send(origin, group, message):
    data = f"{origin}@{group}>{message}\n".encode()  # Verpackt Daten im notwendigen Format (origin@origingroup>target@targetgroup:message\n)
    print(data.decode())                             # schreibt Daten in die Konsole - todo schreiben in Log Datei
    for out_if in interfaces:                        # geht alle Interfaces durch
        out_if.write(data)                           # Daten senden


async def read(in_if):
    return (await in_if.readuntil(b'>')).decode()[:-1], (await in_if.readuntil(b'\n')).decode()[:-1]


async def handle(in_if, out_if):
    group = (await in_if.readuntil(b'\n')).decode()[:-1]  # get Group Name
    interfaces[out_if] = group

    try:
        while not in_if.at_eof():
            origin, message = await read(in_if)
            send(origin, group, message)
            await out_if.drain()
    except Exception as e: print("Error", group, e)
    finally:
        interfaces.pop(out_if)
        out_if.close()


async def main():
    server = await asyncio.start_unix_server(handle, PATH)
    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')
    async with server:
        await server.serve_forever()

asyncio.run(main())
