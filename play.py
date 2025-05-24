from pydub import AudioSegment
import json
import os
import simpleaudio as sa

def play_voice(text_list, voice, second):
    json_path = 'Voice Editor聲庫/' + voice + '/voice-oto.json'
    if not os.path.exists(json_path):
        print(f"JSON 文件 {json_path} 不存在")
        return

    with open(json_path, 'r', encoding='utf-8') as voice_oto_load:
        voice_oto = json.loads(voice_oto_load.read())

    for i in range(len(text_list)):
        if voice_oto.get("Voice-language") == 'zh':
            for text_text in range(len(text_list[i])):
                now_text = text_list[i][text_text]
                if text_text < len(text_list[i]) - 1:  # 确保索引不会超出范围
                    next_text = text_list[i][text_text + 1]
                    if now_text == 'z' and next_text == 'h':
                        play_audio('Voice Editor聲庫/' + voice + '/' + voice_oto.get("Voice-speech-initials", {}).get("zh", ""), second)
                        continue
                    elif now_text == 'y' and next_text == 'u':
                        play_audio('Voice Editor聲庫/' + voice + '/' + voice_oto.get("Voice-speech-initials", {}).get("yu", ""), second)
                        continue
                    elif now_text == 'y' and next_text == 'i':
                        play_audio('Voice Editor聲庫/' + voice + '/' + voice_oto.get("Voice-speech-initials", {}).get("yi", ""), second)
                        continue
                if now_text in voice_oto.get("Voice-speech-initials", {}):
                    play_audio('Voice Editor聲庫/' + voice + '/' + voice_oto.get("Voice-speech-initials", {}).get(now_text, ""), second)
        elif voice_oto.get("Voice-language") == 'jp':
            for text_text in range(len(text_list[i])):
                now_text = text_list[i][text_text]
                if now_text in voice_oto.get("Voice-speech-hiragana", {}):
                    play_audio('Voice Editor聲庫/' + voice + '/' + voice_oto.get("Voice-speech-hiragana", {}).get(now_text, ""), second)

def play_audio(file_path, second):
    # 检查文件是否存在
    if not os.path.exists(file_path):
        print(f"文件 {file_path} 不存在")
        return

    # 加载音频文件
    audio = AudioSegment.from_file(file_path)
    # 只播放前一秒
    one_second_audio = audio[:second * 1000]  # 前1000毫秒（即1秒）

    # 将音频片段转换为 WAV 格式并播放
    wav_data = one_second_audio.raw_data
    play_obj = sa.play_buffer(wav_data, num_channels=one_second_audio.channels, bytes_per_sample=one_second_audio.sample_width, sample_rate=one_second_audio.frame_rate)
    play_obj.wait_done()  # 等待音频播放完成

#play_voice(["い", "う", "え", "お", "か", "き", "く", "け", "こ"], "匿名L(默认)",1)