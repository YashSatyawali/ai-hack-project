import sounddevice as sd
import numpy as np
import whisper
import wave
import signal
import sys
from datetime import datetime
import time

# Audio settings
SAMPLE_RATE = 16000
CHANNELS = 1

# Timestamped filenames
start_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
AUDIO_FILENAME = f"{start_time}_meeting_recording.wav"
TXT_FILENAME = f"{start_time}_meeting_transcription.txt"
SRT_FILENAME = f"{start_time}_meeting_transcription.srt"

# Buffer to store audio
recording = []

# Ctrl+C handler
def signal_handler(sig, frame):
    print("\n⏹️ Stopping recording...")
    save_recording()
    transcribe_audio()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Callback for sounddevice
def callback(indata, frames, time_info, status):
    if status:
        print(status, file=sys.stderr)
    recording.append(indata.copy())

def save_recording():
    audio_data = np.concatenate(recording, axis=0)
    with wave.open(AUDIO_FILENAME, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(2)  # 16-bit
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes((audio_data * 32767).astype(np.int16).tobytes())
    print(f"🎧 Audio saved to {AUDIO_FILENAME}")

def format_timestamp(seconds: float) -> str:
    millis = int((seconds - int(seconds)) * 1000)
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"

def transcribe_audio():
    print("🔎 Transcribing with Whisper...")
    model = whisper.load_model("base")  # tiny/base/small/medium/large
    result = model.transcribe(AUDIO_FILENAME, verbose=True)

    # Save plain text
    with open(TXT_FILENAME, "w", encoding="utf-8") as f:
        f.write(result["text"])
    print(f"✅ Transcription saved to {TXT_FILENAME}")

    # Save SRT
    with open(SRT_FILENAME, "w", encoding="utf-8") as f:
        for i, segment in enumerate(result["segments"], start=1):
            start = format_timestamp(segment["start"])
            end = format_timestamp(segment["end"])
            text = segment["text"].strip()
            f.write(f"{i}\n{start} --> {end}\n{text}\n\n")
    print(f"🎬 Subtitle file saved to {SRT_FILENAME}")

if __name__ == "__main__":
    print("🎙️ Recording... (Press CTRL+C to stop)")
    try:
        with sd.InputStream(samplerate=SAMPLE_RATE, channels=CHANNELS, callback=callback):
            while True:
                time.sleep(0.1)  # keeps CPU low
    except KeyboardInterrupt:
        signal_handler(None, None)
