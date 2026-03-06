import asyncio
import websockets
import json

async def test_connect():
    uri = "ws://127.0.0.1:65520"
    try:
        async with websockets.connect(uri) as websocket:
            print("Successfully connected to websocket")
            
            # Send a handshake-like message
            handshake = {
                "id": 1,
                "action": "request",
                "name": "remixd",
                "payload": ["remixd", ""]
            }
            await websocket.send(json.dumps(handshake))
            print(f"Sent: {handshake}")
            
            response = await websocket.recv()
            print(f"Received: {response}")
            
            # Try a list call
            list_call = {
                "id": 2,
                "action": "request",
                "name": "remixd",
                "payload": ["list", ["/"]]
            }
            await websocket.send(json.dumps(list_call))
            print(f"Sent: {list_call}")
            
            response = await websocket.recv()
            print(f"Received: {response}")
            
    except Exception as e:
        print(f"Failed to connect or talk: {e}")

asyncio.run(test_connect())
