import socket
import os
import resource

def print_limits(prefix=""):
    soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
    print(f"{prefix} ulimit values: soft={soft}, hard={hard}")

def main():
    print("====== Enclave Starting ======")
    print_limits("Initial")

    # 尝试修改限制
    try:
        #resource.setrlimit(resource.RLIMIT_NOFILE, (65535, 65535))
        print_limits("After setrlimit")
    except Exception as e:
        print(f"Failed to set limit: {e}")

    AF_VSOCK = 40
    sock = socket.socket(AF_VSOCK, socket.SOCK_STREAM)
    port = 5000
    sock.bind((socket.VMADDR_CID_ANY, port))
    sock.listen(1)
    print(f"Listening on port {port}")

    while True:
        conn, addr = sock.accept()
        print("====== New Connection ======")
        print_limits("Connection time")
        print(f"Accepted connection from {addr}")
        conn.send(b"Hello from enclave!")
        conn.close()

if __name__ == "__main__":
    main()

