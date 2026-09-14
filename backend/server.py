import asyncio
import websockets
import json
import threading
import logging

# Suppress annoying "invalid Connection header" tracebacks from non-websocket requests
logging.getLogger("websockets.server").setLevel(logging.CRITICAL)

class HologramServer:
    def __init__(self):
        self.clients = set()
        self.running = True

    async def register(self, websocket):
        self.clients.add(websocket)
        try:
            await websocket.wait_closed()
        finally:
            self.clients.remove(websocket)

    async def broadcast(self, message):
        if self.clients:
            await asyncio.gather(*[client.send(message) for client in self.clients])

    async def main(self):
        # Voice Recognition has been moved completely to the frontend (Web Speech API)
        # to eliminate delay and improve performance.
        
        async with websockets.serve(self.register, "localhost", 8765):
            print("WebSocket Server started on ws://localhost:8765")
            print("NOTE: Voice and Gesture recognition are now handled by the browser directly!")
            while self.running:
                await asyncio.sleep(0.1) # Keep the server running

if __name__ == "__main__":
    server = HologramServer()
    try:
        asyncio.run(server.main())
    except KeyboardInterrupt:
        server.running = False
        print("Server stopped.")

