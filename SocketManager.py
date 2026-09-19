from Receive import Receive
from Broadcast import Broadcast

class SocketManager: # Tiny class built to make network swapping easy and offering a single object for signal sending/receiving.
    def __init__(self):
        self.receiver = Receive() # Instantiates sockets with default arguements.
        self.broadcaster = Broadcast()

    def change_network(self, target_address): # No longer two lines! Actually has a somewhat significant feature now with the whole validation thing.
        if not self.validate_network(target_address): # Let's first make sure the address is valid before we try to use it.
            print("Invalid network address: " + target_address + ".")
            return False # Failed.
        self.broadcaster.close()
        self.broadcaster = Broadcast(target_address)
        return True # Allows us to check if the network change went through back in the main file.

    def receive(self): # Wrapper function for receiving data.
        return self.receiver.receive_data()

    def broadcast(self, equipment_id): # Wrapper function for sending data.
        self.broadcaster.broadcast_equipment_code(equipment_id)

    def validate_network(self, target_address): # Makes sure that the entered address is possible.
        # Divide into 4 parts:
        parts = target_address.split('.')
        if len(parts) != 4:
            return False # Nope (not 4 parts).
        # Check Limits:
        for part in parts:
            if not part.isdigit():
                return False # Nope (not a number).
            if int(part) < 0 or int(part) > 255:
                return False # Nope (out of range).
        # Success:
        return True