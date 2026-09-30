# Ethernet Packet Loss Test

This project tests UDP packet transmission and packet loss over a physical Ethernet connection using two USB Ethernet interfaces connected by an Ethernet cable.

---

## 1. Hardware Setup

The test uses:

- Laptop
- Waveshare USB-HUB-3U-ETH
- FLA-100U(A6G) USB Ethernet adapter
- Ethernet cable

The physical connection is:

```text
USB-HUB-3U-ETH
       |
       | Ethernet port
       |
       +========== Ethernet cable ==========+
                                             |
                                             |
                                      FLA-100U(A6G)
[200~# 1. Check USB devices
lsusb

# 2. Find Ethernet interfaces
ip link

# 3. Create two isolated networking environments
sudo ip netns add eth_side_a
sudo ip netns add eth_side_b

# 4. Put the two physical Ethernet interfaces into them
sudo ip link set enx00e04c362ee6 netns eth_side_a
sudo ip link set enx00e04c36003d netns eth_side_b

# 5. Enable the interfaces
sudo ip netns exec eth_side_a ip link set enx00e04c362ee6 up
sudo ip netns exec eth_side_b ip link set enx00e04c36003d up

# 6. Assign IP addresses
sudo ip netns exec eth_side_a ip addr add 192.168.10.1/24 dev enx00e04c362ee6
sudo ip netns exec eth_side_b ip addr add 192.168.10.2/24 dev enx00e04c36003d

# 7. Test basic connectivity
sudo ip netns exec eth_side_a ping -c 10 192.168.10.2

# 8. Create test directory
mkdir -p ~/ethernet_packet_test
cd ~/ethernet_packet_test

# 9. Start UDP echo server
sudo ip netns exec eth_side_b python3 ~/ethernet_packet_test/echo_server.py

# 10. In another terminal, start packet test
sudo ip netns exec eth_side_a python3 ~/ethernet_packet_test/packet_test.py

# 11. Stop with Ctrl+C~                                                       EOF

