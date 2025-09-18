import pyfirmata2
import time

TONE_CMD = 0x7E

def play_tone(board, pin, freq, duration):
    """음계 재생 함수"""
    data = [
        pin,
        freq & 0x7F, (freq >> 7) & 0x7F,
        duration & 0x7F, (duration >> 7) & 0x7F
    ]
    board.send_sysex(TONE_CMD, data)

# 음계 주파수 정의
NOTES = {
    'C4': 261, 'D4': 294, 'E4': 330, 'F4': 349,
    'G4': 392, 'A4': 440, 'B4': 494, 'C5': 523,
    'REST': 0  # 쉼표
}

# 각 음표에 연결된 LED 핀 번호 맵핑
LED_PINS = {
    'C4': 9, 'D4': 10, 'E4': 11, 'F4': 12,
    'G4': 13, 'A4': 4, 'B4': 5, 'C5': 6
}

# 반짝반짝 작은별 악보 (음표, 박자)
TWINKLE_STAR = [
    ('C4', 1), ('C4', 1), ('G4', 1), ('G4', 1),
    ('A4', 1), ('A4', 1), ('G4', 2),
    ('F4', 1), ('F4', 1), ('E4', 1), ('E4', 1),
    ('D4', 1), ('D4', 1), ('C4', 2),
    ('G4', 1), ('G4', 1), ('F4', 1), ('F4', 1),
    ('E4', 1), ('E4', 1), ('D4', 2),
    ('G4', 1), ('G4', 1), ('F4', 1), ('F4', 1),
    ('E4', 1), ('E4', 1), ('D4', 2),
]

def play_melody(board, speaker_pin, melody, bpm=120):
    """멜로디 재생 함수"""
    beat_ms = int(60000 / bpm)

    print(f"🎵 BPM {bpm}로 멜로디 재생 시작...")

    for note, beats in melody:
        freq = NOTES[note]
        duration_ms = int(beat_ms * beats)

        # 현재 음에 해당하는 LED 핀을 가져옵니다.
        led_pin = LED_PINS.get(note)

        if freq > 0:  # 음표
            sound_duration = int(duration_ms * 0.8)
            play_tone(board, speaker_pin, freq, sound_duration)
            
            if led_pin is not None:
                board.digital[led_pin].write(1)  # 💡 해당 음의 LED 켜기
            
            print(f"♪ {note} ({freq}Hz) - {beats}박자")
        else:  # 쉼표
            print(f"♫ 쉼표 - {beats}박자")
        
        time.sleep(duration_ms / 1000)

        # 음표가 끝난 후 LED 끄기
        if freq > 0 and led_pin is not None:
            board.digital[led_pin].write(0) # 💡 해당 음의 LED 끄기

    print("🎉 연주 완료!")

# Arduino 연결
board = pyfirmata2.Arduino('COM8')

# Iterator 시작 (필수!)
it = pyfirmata2.util.Iterator(board)
it.start()

# LED 핀들을 모두 OUTPUT 모드로 설정
for pin in LED_PINS.values():
    board.digital[pin].mode = pyfirmata2.OUTPUT

print("🎼 반짝반짝 작은별 무한 재생")
print("Ctrl+C로 종료")

try:
    while True:
        play_melody(board, 8, TWINKLE_STAR, bpm=100)
        time.sleep(3)
        
except KeyboardInterrupt:
    print("\n🎵 연주 중단")
    
finally:
    # 프로그램 종료 시 모든 LED 끄기
    for pin in LED_PINS.values():
        board.digital[pin].write(0)
    board.exit()
    print("🔌 Arduino 연결 종료")