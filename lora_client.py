#!/usr/bin/env python3
import time
from SX127x.LoRa import *
from SX127x.board_config import BOARD

# 初始化板子設定
BOARD.setup()

class LoRaTransmitter(LoRa):
    def __init__(self, verbose=False):
        super(LoRaTransmitter, self).__init__(verbose)
        self.set_mode(MODE.STDBY)
        self.set_pa_config(pa_select=1)
    
    def on_tx_done(self):
        print("傳送完成")
        self.set_mode(MODE.STDBY)

# 建立 LoRa 物件並設定基本參數
lora = LoRaTransmitter(verbose=False)
lora.set_mode(MODE.STDBY)
lora.set_frequency(915.0)  # 根據地區調整頻率
lora.set_pa_config()

filename = "audio.wav"   # 要傳送的 WAV 檔案
packet_size = 200        # 每個封包大小

try:
    with open(filename, "rb") as f:
        while True:
            data = f.read(packet_size)
            if not data:
                print("檔案傳輸完畢")
                break
            # 將資料轉換成 list 後寫入 payload
            lora.write_payload(list(data))
            # 設定進入 TX 模式以發送封包
            lora.set_mode(MODE.TX)
            # 等待一段時間，讓傳送完成（實際上可依 on_tx_done 事件做進一步處理）
            time.sleep(0.1)
except Exception as e:
    print("發生錯誤:", e)
finally:
    BOARD.teardown()
