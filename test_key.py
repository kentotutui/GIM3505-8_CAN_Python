import can
import struct
import time

bus = can.interface.Bus(channel='can0', interface='socketcan')

def send_command(can_id, data):
    msg = can.Message(arbitration_id=can_id, data=data, is_extended_id=False)
    bus.send(msg)
    print(f"Sent: {msg}")

def float_to_bytes(f):
    return list(struct.pack('<f', f))

def duration_to_bytes(ms):
    return [ms & 0xFF, (ms >> 8) & 0xFF, (ms >> 16) & 0xFF]

CAN_ID = 0x002

# モータ起動（必須）
send_command(CAN_ID, [0x91] + [0x00]*7)
time.sleep(0.1)

# 入力待機
user_input = input("モータを動かすには 'a' と入力してください: ")

if user_input.lower() == 'a':
    # 位置制御コマンド：30度、2000msかけて回転
    target_angle_deg = 30.0
    move_time_ms = 2000

    angle_bytes = float_to_bytes(target_angle_deg)
    duration_bytes = duration_to_bytes(move_time_ms)

    send_command(CAN_ID, [0x95] + angle_bytes + duration_bytes)
    time.sleep(3)
else:
    print("キャンセルされました。")

# モータ停止
send_command(CAN_ID, [0x92] + [0x00]*7)
