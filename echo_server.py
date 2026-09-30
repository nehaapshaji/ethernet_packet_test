import socket

IP = "192.168.10.2"
PORT = 5000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((IP, PORT))

print(f"Echo server listening on {IP}:{PORT}")

while True:
    data, address = sock.recvfrom(2048)

    print(f"Received {data.decode()} from {address}")

    sock.sendto(data, address)
