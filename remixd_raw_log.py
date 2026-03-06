"""
Remixd Raw Message Logger - captures EXACT bytes from Remix IDE
"""
import asyncio
import json
import websockets

HOST = "127.0.0.1"
PORT = 65520

async def client_handler(websocket):
    addr = websocket.remote_address
    print(f"\n[+] Connected from {addr[0]}:{addr[1]}")
    try:
        async for message in websocket:
            print(f"\n=== RAW MESSAGE ===")
            print(repr(message))
            print(f"=== PARSED ===")
            try:
                parsed = json.loads(message)
                print(json.dumps(parsed, indent=2))
            except:
                print("(not valid JSON)")
            print(f"==================")
            # Send a generic success response to keep connection alive
            try:
                msg = json.loads(message)
                resp = {"id": msg.get("id"), "jsonrpc": "2.0", "result": True}
                await websocket.send(json.dumps(resp))
            except:
                pass
    except Exception as e:
        print(f"Error: {e}")
    print("[-] Disconnected")

async def main():
    print(f"[*] Raw logger on ws://{HOST}:{PORT}")
    async with websockets.serve(client_handler, HOST, PORT):
        await asyncio.Future()

asyncio.run(main())
