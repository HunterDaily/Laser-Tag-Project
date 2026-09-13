import socket

class Receive:
    def __init__(self, receive_ip = "0.0.0.0", receive_port = 7501):
        self.receive_ip = receive_ip
        self.receive_port = receive_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.receive_ip, self.receive_port))
    
    def receive_data(self):
        try:
            data, addr = self.sock.recvfrom(4096)  # buffer size is 4096 bytes
            print(f"Received data: {data.decode('utf-8')} from {addr}")
            return data.decode('utf-8')
        except Exception as e:
            print(f"Error occurred while receiving data: {e}")
            return None
        
    def close(self):
        self.sock.close()