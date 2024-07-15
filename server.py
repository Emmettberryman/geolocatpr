import sys
import struct

# Simulate SPIKE Prime environment
class SimulatedBluetooth:
    FLAG_NOTIFY = 0x10
    FLAG_WRITE = 0x08

    class UUID:
        def __init__(self, uuid):
            self.uuid = uuid

    class BLE:
        def gap_advertise(self, interval_us, adv_data=None):
            print(f"Simulated: Advertising with interval {interval_us}")

    class Peripheral:
        def add_service(self, uuid):
            print(f"Simulated: Added service {uuid.uuid}")

        def add_characteristic(self, uuid, flags):
            flag_names = []
            if flags & SimulatedBluetooth.FLAG_NOTIFY:
                flag_names.append("NOTIFY")
            if flags & SimulatedBluetooth.FLAG_WRITE:
                flag_names.append("WRITE")
            print(f"Simulated: Added characteristic {uuid.uuid} with flags {', '.join(flag_names)}")

        def on_write(self, callback):
            print(f"Simulated: Set on_write callback")

class SimulatedHub:
    class light:
        @staticmethod
        def on(color='green'):
            print(f"Simulated: Light on with color {color}")

# Use simulated modules if not on SPIKE Prime
if 'hub' not in sys.modules:
    print("Running in simulated environment")
    bluetooth = SimulatedBluetooth()
    hub = SimulatedHub()
else:
    import bluetooth
    from hub import light

# Your original code starts here
UART_UUID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
TX_UUID = bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E")
RX_UUID = bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E")

ble = bluetooth.BLE()
uart = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")

def on_rx(data):
    print("Received:", data.decode() if isinstance(data, bytes) else data)

server = bluetooth.Peripheral()
server.add_service(uart)
server.add_characteristic(TX_UUID, bluetooth.FLAG_NOTIFY)
rx = server.add_characteristic(RX_UUID, bluetooth.FLAG_WRITE)
rx.on_write(on_rx)

ble.gap_advertise(100, bytearray("\x02\x01\x06" + struct.pack("<BHBH", 0x3, UART_UUID, 0x3, uart)))

hub.light.on(color='green')

print("Server is running (simulated)")
while True:
    # Simulate receiving data
    simulated_data = input("Enter simulated data to receive (or 'quit' to exit): ")
    if simulated_data.lower() == 'quit':
        break
    on_rx(simulated_data)