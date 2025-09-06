import pyaudio
import wave
import whisper
import signal
import sys
from datetime import datetime
import os
from pathlib import Path

start_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


start_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

BASE_DIR = Path(__file__).resolve().parent

media_saved = BASE_DIR / "data_recived" / "from_speaker" / f"data_at_{start_time}"

media_saved.mkdir(parents = True, exist_ok=True)

# --- Audio Recording Settings ---
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1  # Whisper prefers mono
RATE = 16000  # Whisper prefers 16000Hz

# Timestamped filenames
AUDIO_FILENAME = media_saved / f"{start_time}_meeting_recording.wav"
TXT_FILENAME = media_saved / f"{start_time}_meeting_transcription.txt"
SRT_FILENAME = media_saved / f"{start_time}_meeting_transcription.srt"

# Buffers
p = None
stream = None
frames = []

# Handle Ctrl+C (graceful exit)
def signal_handler(sig, frame):
    print("\n Stopping recording...")
    cleanup()
    save_audio()
    transcribe_audio()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def cleanup():
    if stream:
        stream.stop_stream()
        stream.close()
    if p:
        p.terminate()

def save_audio():
    print(f" Saving audio to {AUDIO_FILENAME}...")
    wf = wave.open(str(AUDIO_FILENAME), 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    print(" Audio saved.")

def format_timestamp(seconds: float) -> str:
    millis = int((seconds - int(seconds)) * 1000)
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"

def transcribe_audio():
    print(" Transcribing with Whisper...")
    model = whisper.load_model("base")  # You can change this to tiny/small/medium/large
    result = model.transcribe(str(AUDIO_FILENAME), verbose=True)

    # Save plain text
    with open(TXT_FILENAME, "w", encoding="utf-8") as f:
        f.write(result["text"])
    print(f" Transcription saved to {TXT_FILENAME}")

    # Save SRT subtitles
    with open(SRT_FILENAME, "w", encoding="utf-8") as f:
        for i, segment in enumerate(result["segments"], start=1):
            start = format_timestamp(segment["start"])
            end = format_timestamp(segment["end"])
            text = segment["text"].strip()
            f.write(f"{i}\n{start} --> {end}\n{text}\n\n")
    print(f" Subtitle file saved to {SRT_FILENAME}")

# --- Main Recording Logic ---
if __name__ == "__main__":
    try:
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        print(" Recording... Press Ctrl+C to stop.")

        while True:
            data = stream.read(CHUNK)
            frames.append(data)

    except KeyboardInterrupt:
        signal_handler(None, None)

    except Exception as e:
        print(f" Error: {e}")
        cleanup()
