"""A local HTTP proxy that checks Basic auth and tunnels CONNECT, used to test the example without a real proxy account."""
import base64, select, socket, sys, threading
USER, PASSWORD, PORT = sys.argv[1], sys.argv[2], int(sys.argv[3])
EXPECTED = "Basic " + base64.b64encode(f"{USER}:{PASSWORD}".encode()).decode()
def handle(client):
    data = b""
    while b"\r\n\r\n" not in data:
        chunk = client.recv(4096)
        if not chunk: return client.close()
        data += chunk
    head = data.split(b"\r\n\r\n")[0].decode("latin1").split("\r\n")
    auth = next((h.split(":", 1)[1].strip() for h in head[1:] if h.lower().startswith("proxy-authorization:")), None)
    print("REQUEST", head[0], "| auth ok" if auth == EXPECTED else "| auth BAD", flush=True)
    if auth != EXPECTED:
        client.sendall(b"HTTP/1.1 407 Proxy Authentication Required\r\nProxy-Authenticate: Basic\r\nContent-Length: 0\r\n\r\n"); return client.close()
    method, target, _ = head[0].split(" ")
    if method != "CONNECT":
        client.sendall(b"HTTP/1.1 501 Not Implemented\r\nContent-Length: 0\r\n\r\n"); return client.close()
    host, port = target.rsplit(":", 1)
    remote = socket.create_connection((host, int(port)), timeout=30)
    client.sendall(b"HTTP/1.1 200 Connection Established\r\n\r\n")
    socks = [client, remote]
    while True:
        r, _, _ = select.select(socks, [], [], 30)
        if not r: break
        for s in r:
            b = s.recv(65536)
            if not b: client.close(); remote.close(); return
            (remote if s is client else client).sendall(b)
srv = socket.socket(); srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
srv.bind(("127.0.0.1", PORT)); srv.listen(16); print("mock proxy on", PORT, flush=True)
while True:
    c, _ = srv.accept(); threading.Thread(target=handle, args=(c,), daemon=True).start()
