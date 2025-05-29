import socket
import resource

soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
print(f"Current limits: soft={soft}, hard={hard}")

def main():
    AF_VSOCK = 40
    sock = socket.socket(AF_VSOCK, socket.SOCK_STREAM)
    enclave_cid = 24  # 需要根据实际 enclave CID 修改
    port = 5000
    
    try:
        sock.connect((enclave_cid, port))
        data = sock.recv(1024)
        print(f"Received: {data.decode()}")
    finally:
        sock.close()

if __name__ == "__main__":
    main()

