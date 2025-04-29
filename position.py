import can
import time
import pygame
import struct
import signal
import sys

# === 設定 ===
NODE_ID = 0x02  # GIM MotorのCAN ID (デフォルト2?)

CAN_ID = NODE_ID  # GIMはこのまま使う

CMD_START_MOTOR = 0x91
CMD_STOP_MOTOR = 0x92
CMD_POSITION_CONTROL = 0x95

# === CANインタフェース ===
bus = can.interface.Bus(channel='can0', interface='socketcan')

# === CAN送信関数 ===
def send_can_cmd(cmd_byte, data_bytes=None):
    if data_bytes is None:
        data_bytes = [0] * 7
    data = [cmd_byte] + data_bytes  # コマンドを先頭に
    msg = can.Message(arbitration_id=CAN_ID, data=data, is_extended_id=False)
    bus.send(msg)
    print(f"[CAN] Sent: cmd=0x{cmd_byte:02X}, data={data}")
    time.sleep(0.05)

# === 初期化 ===
# モーター起動
send_can_cmd(CMD_START_MOTOR)
print("[CAN] Sent: Start Motor")
time.sleep(1.0)

# === Pygame初期化 ===
pygame.init()
screen = pygame.display.set_mode((300, 100))
pygame.display.set_caption("GIM Motor Position Control")

# Ctrl+Cなどの例外処理
def signal_handler(sig, frame):
    print('Exiting...')
    send_can_cmd(CMD_STOP_MOTOR)
    pygame.quit()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

current_position = 0.0  # 単位はラジアン
running = True
clock = pygame.time.Clock()

def send_position(pos_rad):
    pos_bytes = struct.pack('<f', pos_rad)  # float32リトルエンディアン
    duration_ms = 1000  # 1秒間で動く（適宜変更可）
    duration_bytes = duration_ms.to_bytes(3, byteorder='little')  # 24bit
    data = list(pos_bytes + duration_bytes)
    send_can_cmd(CMD_POSITION_CONTROL, data)
    print(f"[CAN] Sent position: {pos_rad:.2f} rad")

# === メインループ ===
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP]:
        current_position += 0.1  # ラジアン単位、少しずつ動かす
        send_position(current_position)
        time.sleep(0.1)

    elif keys[pygame.K_DOWN]:
        current_position -= 0.1
        send_position(current_position)
        time.sleep(0.1)

    clock.tick(60)

# === 終了時 ===
send_can_cmd(CMD_STOP_MOTOR)
pygame.quit()
