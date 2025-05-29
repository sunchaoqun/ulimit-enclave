import socket
import os
import resource
import time

def print_limits(prefix=""):
    soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
    print(f"{prefix} ulimit values: soft={soft}, hard={hard}")

def main():
    print("====== Enclave Starting ======")
    print_limits("Initial")

    # 尝试设置一个较小的限制，比如10
    try:
        resource.setrlimit(resource.RLIMIT_NOFILE, (10, 10))
        print_limits("After setrlimit")
    except Exception as e:
        print(f"Failed to set limit: {e}")

    # 保存所有创建的socket
    sockets = []
    
    try:
        # 创建主监听socket
        AF_VSOCK = 40
        main_sock = socket.socket(AF_VSOCK, socket.SOCK_STREAM)
        port = 5000
        main_sock.bind((socket.VMADDR_CID_ANY, port))
        main_sock.listen(1)
        print(f"Main socket created, listening on port {port}")

        # 尝试创建多个测试socket直到失败
        count = 0
        while True:
            try:
                test_sock = socket.socket(AF_VSOCK, socket.SOCK_STREAM)
                sockets.append(test_sock)
                count += 1
                print(f"Successfully created socket #{count}")
            except Exception as e:
                print(f"Failed to create socket #{count+1}: {e}")
                break

        print(f"Total sockets created: {count}")
        
        # 保持程序运行一段时间
        while True:
            conn, addr = main_sock.accept()
            print(f"Accepted connection from {addr}")
            conn.send(b"Hello from enclave!")
            conn.close()

    except Exception as e:
        print(f"Error: {e}")
    finally:
        # 清理所有socket
        for sock in sockets:
            try:
                sock.close()
            except:
                pass

if __name__ == "__main__":
    main()

