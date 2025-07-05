import socket
import threading
import time

def client_thread(name, delay):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('172.16.16.101', 45000))
        print(f"[{name}] Connected to server")

        s.sendall(b"TIME\r\n")
        response = s.recv(1024).decode('utf-8')
        print(f"[{name}] Received: {response.strip()}")

        time.sleep(delay)  # Simulasi client nunggu

        s.sendall(b"QUIT\r\n")
        s.close()
        print(f"[{name}] Disconnected")
    except Exception as e:
        print(f"[{name}] Error: {e}")

def main():
    threads = []
    for i in range(3):
        t = threading.Thread(target=client_thread, args=(f"Client-{i+1}", 5))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

if __name__ == "__main__":
    main()