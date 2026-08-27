import socket

host = "smtp.gmail.com"
ports = [25, 465, 587]

for port in ports:
    print(f"Connecting to {host}:{port} via plain TCP socket (3s timeout)...", flush=True)
    try:
        s = socket.create_connection((host, port), timeout=3)
        print(f"TCP connection to {host}:{port} SUCCEEDED!", flush=True)
        s.close()
    except Exception as e:
        print(f"TCP connection to {host}:{port} FAILED: {e}", flush=True)
