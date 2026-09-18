from Receive import Receive
from Broadcast import Broadcast

class SocketManager: # Tiny class built to make network swapping easy and offering a single object for signal sending/receiving.
    def __init__(self):
        self.receiver = Receive() # Instantiates sockets with default arguements.
        self.broadcaster = Broadcast()

    def change_network(self, target_address): # Turned out to literally be two lines, so one could argue the class is redundant, but it's my first little git commit and therefore my baby.
        self.broadcaster.close()
        self.broadcaster = Broadcast(target_address)

    def receive(self): # Wrapper function for receiving data.
        return self.receiver.receive_data()

    def broadcast(self, equipment_id): # Wrapper function for sending data.
        self.broadcaster.broadcast_equipment_code(equipment_id)