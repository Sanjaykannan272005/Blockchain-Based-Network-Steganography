"""
Remixd-Compatible WebSocket Server (v2.4 - Ultimate Stability)
=============================================================
Designed to be compatible with all modern Remix versions.
Handles 'remixd', 'shared-folder', and 'fs' service calls.

Usage: python remixd_server.py
"""

import asyncio
import json
import os
import sys
import websockets
import traceback

SHARED_FOLDER = r"e:\Projects\steganography"
HOST = "0.0.0.0"
PORT = 65520

def norm(rel_path):
    if not rel_path or rel_path in ('.', '/', '\\'):
        return SHARED_FOLDER
    # Handle Windows paths correctly
    rel_path = str(rel_path).replace('/', os.sep).lstrip(os.sep)
    return os.path.normpath(os.path.join(SHARED_FOLDER, rel_path))

def get_dir_entries(folder_path):
    print(f"       [FS] Listing: {folder_path}")
    entries = {}
    try:
        if not os.path.exists(folder_path):
            return {}
        for entry in os.listdir(folder_path):
            if entry.startswith('.') or entry in ('node_modules', '__pycache__', '.git', '.gemini'):
                continue
            full = os.path.join(folder_path, entry)
            rel = os.path.relpath(full, SHARED_FOLDER).replace('\\', '/')
            entries[rel] = {
                'isDirectory': os.path.isdir(full),
                'isReadOnly': False
            }
    except Exception as e:
        print(f"       [!] error listing: {e}")
    return entries

def handle_fs_call(func, args):
    print(f"       [FS] Call: {func} Args: {args}")
    if func in ('list', 'fileList', 'resolveDirectory', 'dirList'):
        path = args[0] if args else ''
        return get_dir_entries(norm(path))
    elif func in ('get', 'getFile', 'readFile'):
        path = args[0] if args else ''
        abs_path = norm(path)
        if os.path.isfile(abs_path):
            with open(abs_path, 'r', encoding='utf-8', errors='replace') as f:
                return f.read()
    elif func in ('set', 'setFile', 'writeFile'):
        path, content = args[0], args[1]
        abs_path = norm(path)
        os.makedirs(os.path.dirname(abs_path), exist_ok=True)
        with open(abs_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"       [FS] Created/Updated: {path}")
        return True
    elif func == 'exists':
        return os.path.exists(norm(args[0] if args else ''))
    elif func == 'isDirectory':
        return os.path.isdir(norm(args[0] if args else ''))
    return None

async def client_handler(websocket):
    addr = websocket.remote_address
    print(f"\n[+] Accepted connection from {addr[0]}:{addr[1]}")
    try:
        async for raw in websocket:
            try:
                msg = json.loads(raw)
            except: 
                print(f"  [!] Invalid JSON: {raw[:100]}")
                continue

            msg_id = msg.get('id')
            action = msg.get('action', '')
            name = msg.get('name', '')
            payload = msg.get('payload', [])

            print(f"  --> {action}:{name} [id={msg_id}]")

            # 1. Handshake / Version Check
            if action == 'request' and name == 'remixd':
                # Official response for 0.6.0
                res = {
                    'id': msg_id, 'action': 'response', 'name': 'remixd',
                    'payload': [None, {"version": "0.6.0", "service": "folder"}]
                }
                await websocket.send(json.dumps(res))
                print(f"  <-- Handshake ACK sent")
                continue

            # 2. Filesystem / Shared Folder service
            if action in ('request', 'call') and name in ('remixd', 'shared-folder', 'fs'):
                if isinstance(payload, list) and payload:
                    func = payload[0]
                    args = payload[1:]
                    if len(args) == 1 and isinstance(args[0], list): args = args[0]
                    
                    try:
                        result = handle_fs_call(func, args)
                        response = {'id': msg_id, 'action': 'response', 'name': name, 'payload': [None, result]}
                    except Exception as e:
                        print(f"  [!] Error: {e}")
                        response = {'id': msg_id, 'action': 'response', 'name': name, 'payload': [str(e), None]}
                    await websocket.send(json.dumps(response))
                    continue

            # 3. Handle calls from other services (e.g. 'hard hat', 'truffle')
            # Just return a null success to prevent hanging
            await websocket.send(json.dumps({'id': msg_id, 'action': 'response', 'name': name, 'payload': [None, None]}))

    except Exception as e:
        print(f"[-] Connection error: {e}")
    finally:
        print(f"[-] Client disconnected")

async def main():
    print("=" * 60)
    print("  Remixd Server v2.4 (The Ultimate Bridge)")
    print(f"  Listening on: ws://0.0.0.0:{PORT}")
    print(f"  Folder:       {SHARED_FOLDER}")
    print("=" * 60)
    async with websockets.serve(client_handler, HOST, PORT):
        print(f"[*] Server ready. Please Connect in Remix IDE.\n")
        await asyncio.Future()

if __name__ == "__main__":
    try: asyncio.run(main())
    except KeyboardInterrupt: print("\n[*] Manual stop.")
    except Exception as e: print(f"[!] Crash: {e}"); traceback.print_exc()
