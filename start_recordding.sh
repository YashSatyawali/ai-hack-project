#!/bin/bash

echo "Running speaker and mic Python script..."
python whisper_test/speaker_transcription.py &

python whisper_test/transcription.py

echo "Both scripts have finished running."
