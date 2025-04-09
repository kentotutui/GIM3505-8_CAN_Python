import can
import struct
import time

bus = can.interface.Bus(channel='can0', interface='socketcan')

def send_command(can_id, data):
    msg = can.Message(arbitration_id=can_id, data=data, is_extended_id=False)
    bus.send(msg)
    print(f"Sent: {msg}")

CAN_ID = 0x001

# モータ起動（必須）
send_command(CAN_ID, [0x91] + [0x00]*7)
time.sleep(0.1)

# 速度設定 (30RPMで1秒間)
speed_bytes = list(struct.pack('<f', 120.0))
duration_bytes = [0xE8, 0x03, 0x00]  # 1000ms
send_command(CAN_ID, [0x94] + speed_bytes + duration_bytes)

time.sleep(2)

# モータ停止
send_command(CAN_ID, [0x92] + [0x00]*7)