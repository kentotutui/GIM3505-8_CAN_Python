import can
import struct
import time
import math

CMD_POSITION_CONTROL = 0x95
CMD_MOTOR_ON = 0x91
CMD_MOTOR_OFF = 0x92

bus = can.interface.Bus(channel='can0', interface='socketcan')

# === CAN送信関数（統一版） ===
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

# === モータ起動（必須） ===
send_can_cmd(CMD_MOTOR_ON)

time.sleep(0.1)

"""
# 速度設定 (120RPMで1秒間) をやりたいならここを使う
speed_bytes = float_to_bytes(120.0)
duration_bytes = duration_to_bytes(1000)  # 1000ms
send_can_cmd(0x94, speed_bytes + duration_bytes)

time.sleep(2)
"""

# === 位置制御コマンド ===
pos_deg = 0
pos_rad = pos_deg / (180 / math.pi)

pos_bytes = float_to_bytes(pos_rad)  # float32リトルエンディアン
duration_ms = 1000  # 1秒間で動く
duration_bytes = duration_to_bytes(duration_ms)  # 24bitリトルエンディアン

send_can_cmd(CMD_POSITION_CONTROL, pos_bytes + duration_bytes)

time.sleep(2)

# === モータ停止 ===
send_can_cmd(CMD_MOTOR_OFF)
