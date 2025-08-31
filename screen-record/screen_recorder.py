import pyscreenrec
from tkinter import *

# Create a ScreenRecorder instance
recorder = pyscreenrec.ScreenRecorder()

def start_recording():
    filename = "recording.mp4"
    print(f"Starting recording... Saved to {filename}")
    recorder.start_recording(filename, 30) # 30 FPS

def stop_recording():
    print("Stopping recording.")
    recorder.stop_recording()
    print("Recording stopped. File saved.")

# Create a GUI window
window = Tk()
window.title("Screen Recorder")
window.geometry("250x100")
window.resizable(False, False)

# Create buttons
start_button = Button(window, text="Start Recording", command=start_recording)
start_button.pack(pady=10)

stop_button = Button(window, text="Stop Recording", command=stop_recording)
stop_button.pack(pady=5)

window.mainloop()
