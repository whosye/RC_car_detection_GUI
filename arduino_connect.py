import serial.tools.list_ports
def WritoToArduino(num,ser):
    # Accepts only nums = [1, 2, 3, 4, 5]
    if num in ['1', '2', '3', '4', '5']:
        command = num
        print(f"Command sent: {command}")
        ser.write(command.encode())
    else:
        print("Invalid input. Accepted values are '1', '2', '3', '4', or '5'.") 

def findArduinoPort():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if "USB-SERIAL" in port.description.upper():
            return port.device
    
