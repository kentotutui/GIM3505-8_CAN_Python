sudo ip link set can0 down
sudo ip link set can0 type can bitrate 500000
sudo ip link set can0 up
#python3 ./gim3505-8.py
#python3 ./test_key.py
python3 ./position.py