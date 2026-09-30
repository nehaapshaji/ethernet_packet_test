import socket
import time

LOCAL_IP = "192.168.10.1"
REMOTE_IP = "192.168.10.2"
PORT = 5000

PACKET_INTERVAL = 0.001   # 10 ms = 100 packets/second

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.bind((LOCAL_IP, 0))

sock.settimeout(1.0)

sequence = 0
sent = 0
received = 0
lost = 0
duplicates = 0
out_of_order = 0

last_received = 0

print("======================================")
print(" Ethernet Continuous Packet Test")
print("======================================")
print(f"Source      : {LOCAL_IP}")
print(f"Destination : {REMOTE_IP}:{PORT}")
print("Rate        : 100 packets/second")
print("--------------------------------------")
print("Press Ctrl+C to stop")
print("--------------------------------------")

try:

    while True:

        sequence += 1

        message = f"SEQ={sequence}".encode()

        sock.sendto(message, (REMOTE_IP, PORT))
        sent += 1

        try:

            data, address = sock.recvfrom(2048)

            text = data.decode()

            if text.startswith("SEQ="):

                received_sequence = int(text.split("=")[1])

                received += 1

                if received_sequence <= last_received:
                    duplicates += 1

                elif received_sequence > last_received + 1:
                    missing = received_sequence - last_received - 1
                    lost += missing

                    print(
                        f"MISSING: packets "
                        f"{last_received + 1} to "
                        f"{received_sequence - 1}"
                    )

                if received_sequence < last_received:
                    out_of_order += 1

                last_received = max(last_received, received_sequence)

        except socket.timeout:

            lost += 1

            print(f"TIMEOUT: packet {sequence}")

        if sequence % 100 == 0:

            print(
                f"Sent={sent}  "
                f"Received={received}  "
                f"Lost={lost}  "
                f"Duplicates={duplicates}  "
                f"OutOfOrder={out_of_order}"
            )

        time.sleep(PACKET_INTERVAL)

except KeyboardInterrupt:

    print("\n")
    print("======================================")
    print(" Test stopped")
    print("======================================")

    print(f"Packets sent     : {sent}")
    print(f"Packets received : {received}")
    print(f"Packets lost     : {lost}")
    print(f"Duplicates       : {duplicates}")
    print(f"Out of order     : {out_of_order}")

    if sent > 0:

        loss_percentage = (lost / sent) * 100

        print(f"Packet loss      : {loss_percentage:.6f}%")

    print("======================================")
