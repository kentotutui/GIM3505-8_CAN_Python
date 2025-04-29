import can
import struct
import time
import math

CMD_POSITION_CONTROL = 0x95

bus = can.interface.Bus(channel='can0', interface='socketcan')

def send_command(can_id, data):
    msg = can.Message(arbitration_id=can_id, data=data, is_extended_id=False)
    bus.send(msg)
    print(f"Sent: {msg}")

# === CAN送信関数 ===
def send_can_cmd(cmd_byte, data_bytes=None):
    if data_bytes is None:
        data_bytes = [0] * 7
    data = [cmd_byte] + data_bytes  # コマンドを先頭に
    msg = can.Message(arbitration_id=CAN_ID, data=data, is_extended_id=False)
    bus.send(msg)
    print(f"[CAN] Sent: cmd=0x{cmd_byte:02X}, data={data}")
    time.sleep(0.05)

def float_to_bytes(f):
    return list(struct.pack('<f', f))

def duration_to_bytes(ms):
    return [ms & 0xFF, (ms >> 8) & 0xFF, (ms >> 16) & 0xFF]

CAN_ID = 0x002

# モータ起動（必須）
send_command(CAN_ID, [0x91] + [0x00]*7)
time.sleep(0.1)

"""
# 速度設定 (30RPMで1秒間)
speed_bytes = list(struct.pack('<f', 120.0))
duration_bytes = [0xE8, 0x03, 0x00]  # 1000ms
send_command(CAN_ID, [0x94] + speed_bytes + duration_bytes)

time.sleep(2)
"""
pos_deg = 180
pos_rad = pos_deg / (180/math.pi)

pos_bytes = struct.pack('<f', pos_rad)  # float32リトルエンディアン
duration_ms = 1000  # 1秒間で動く（適宜変更可）
duration_bytes = duration_ms.to_bytes(3, byteorder='little')  # 24bit
data = list(pos_bytes + duration_bytes)
send_can_cmd(CMD_POSITION_CONTROL, data)

time.sleep(2)

# モータ停止
send_command(CAN_ID, [0x92] + [0x00]*7)