import socket

class Broadcast:
    def __init__(self, broadcast_ip = "127.0.0.255", broadcast_port = 7500):
        self.broadcast_ip = broadcast_ip
        self.broadcast_port = broadcast_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    
    # to be called after player is succesfully added to database
    def broadcast_equipment_code(self, equipment_id):
        message = equipment_id.encode('utf-8')
        try:
            self.sock.sendto(message, (self.broadcast_ip, self.broadcast_port))
            print(f"Broadcasted equipment code {equipment_id} to {self.broadcast_ip}:{self.broadcast_port}")
        except Exception as e:
            print(f"Error occurred while broadcasting equipment code {equipment_id}: {e}")
    
    def close(self):
        self.sock.close()