import socket
import threading
from datetime import datetime

class Server(threading.Thread):
    def __init__(self, port=45000):
        super().__init__()
        self.the_clients = []
        self.socket = None
        self.port = port
        
    def run(self):
        # Create TCP socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Bind to port 45000
        self.socket.bind(('0.0.0.0', self.port))
        self.socket.listen(5)
        
        print(f"Time server listening on port {self.port}")
        
        while True:
            try:
                client_socket, client_address = self.socket.accept()
                print(f"Connection from {client_address}")
                
                # Create new thread for each client
                client_thread = ProcessTheClient(client_socket, client_address)
                client_thread.start()
                
                self.the_clients.append(client_thread)
                
            except Exception as e:
                print(f"Error accepting connection: {e}")
                break

class ProcessTheClient(threading.Thread):
    def __init__(self, connection, address):
        super().__init__()
        self.connection = connection
        self.address = address
        
    def run(self):
        try:
            while True:
                # Receive data (max 1024 bytes)
                data = self.connection.recv(1024)
                
                if not data:
                    break
                
                # Check if data ends with CR+LF (karakter 13 dan 10)
                if len(data) < 2 or data[-2] != 13 or data[-1] != 10:
                    print(f"Invalid data format from {self.address}")
                    break
                
                # Decode and strip CR+LF
                message = data.decode('utf-8').strip()
                print(f"Received from {self.address}: {message}")
                
                # Process TIME command
                if message == "TIME":
                    # Get current time
                    now = datetime.now()
                    time_string = now.strftime("%H:%M:%S")
                    
                    # Format response: "JAM hh:mm:ss" + CR + LF
                    response = f"JAM {time_string}\r\n"
                    
                    # Send response
                    self.connection.send(response.encode('utf-8'))
                    print(f"Sent time to {self.address}: {time_string}")
                    
                # Process QUIT command
                elif message == "QUIT":
                    print(f"Client {self.address} requested disconnect")
                    break
                    
                else:
                    # Invalid command
                    response = "Invalid command\r\n"
                    self.connection.send(response.encode('utf-8'))
                    print(f"Invalid command from {self.address}: {message}")
                    
        except Exception as e:
            print(f"Error processing client {self.address}: {e}")
        finally:
            print(f"Closing connection to {self.address}")
            self.connection.close()

def main():
    # Create and start server
    server = Server(port=45000)
    server.start()
    
    # Keep main thread alive
    try:
        server.join()
    except KeyboardInterrupt:
        print("Server shutting down...")

if __name__ == "__main__":
    main()
