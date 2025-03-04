import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt

# 定義參數設定
config = {
    'sample_rate': 22050,
    'n_mels': 256,
    'n_fft': 1024,
    'hop_length': 256,
    'input_shape': (256, 431, 1),
}

def process_audio(audio_path, config):
    # 1. 載入音訊（自動轉換採樣率）
    y, sr = librosa.load(audio_path, sr=config['sample_rate'])
    
    # 2. 計算 Mel 頻譜圖 (能量譜)
    mel_spec = librosa.feature.melspectrogram(y=y, 
                                              sr=sr, 
                                              n_fft=config['n_fft'], 
                                              hop_length=config['hop_length'], 
                                              n_mels=config['n_mels'])
    # 3. 將能量譜轉換成分貝 (dB) 單位
    mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)
    
    # 4. 調整時間軸長度以符合 config['input_shape'][1] (431)
    target_frames = config['input_shape'][1]
    current_frames = mel_spec_db.shape[1]
    
    if current_frames < target_frames:
        # 若不足則在右側補零
        pad_width = target_frames - current_frames
        mel_spec_db = np.pad(mel_spec_db, ((0, 0), (0, pad_width)), mode='constant')
    elif current_frames > target_frames:
        # 若超過則只取前 target_frames 個 frames
        mel_spec_db = mel_spec_db[:, :target_frames]
    
    # 5. 增加頻道維度 (轉換成 (256, 431, 1))
    mel_spec_db = np.expand_dims(mel_spec_db, axis=-1)
    
    return mel_spec_db, sr

# 主程式
if __name__ == '__main__':
    audio_file = 'your_audio_file.wav'  # 請替換成你的音訊檔案路徑
    mel_spectrogram, sr = process_audio(audio_file, config)
    
    # 印出最終的頻譜圖形狀
    print("輸出形狀：", mel_spectrogram.shape)
    
    # 繪製頻譜圖 (移除頻道維度以便顯示)
    plt.figure(figsize=(10, 6))
    librosa.display.specshow(np.squeeze(mel_spectrogram), 
                             sr=sr, 
                             hop_length=config['hop_length'], 
                             x_axis='time', 
                             y_axis='mel')
    plt.title('Mel 頻譜圖')
    plt.colorbar(format='%+2.0f dB')
    plt.xlabel('時間 (秒)')
    plt.ylabel('頻率 (Mel)')
    plt.show()
