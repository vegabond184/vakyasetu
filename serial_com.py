# import serial
# import pyautogui

# ser = serial.Serial(port='COM12', baudrate=115200, timeout=1)
# while True:
#     line = ser.readline() # Reads until a newline character is encountered
#     print(line.decode())   

#     try:
#         value = int(line.decode())
#         if value > 0:
#             print("right") 
#             pyautogui.press('Delete')

#     except ValueError:
#         pass
   
    


import socket

host = "10.67.60.116"  # The server's hostname or IP address
port = 80        # The port used by the server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
    # s.sendall(b"Hello, world")
while True:
    data = s.recv(1024).decode()
    print(data)