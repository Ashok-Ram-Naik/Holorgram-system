import asyncio
import websockets
import logging

logging.getLogger("websockets.server").setLevel(logging.ERROR)

async def handler(ws):
    pass

async def main():
    async with websockets.serve(handler, 'localhost', 8766):
        print("Test server running")
        await asyncio.sleep(10)

asyncio.run(main())
