import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv(dotenv_path=r'd:/RAJ/Python/project_test/ai-hack-project/.env')

api_key = os.getenv('GEMINI_FLASH_API_KEY')

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-1.5-flash")

# Read transcript from file
with open(r'd:/RAJ/Python/project_test/ai-hack-project/whisper_test/2025-08-24_21-19-24_meeting_transcription.txt', 'r', encoding='utf-8') as f:
    transcript = f.read().strip()


# Ask Gemini to structure the meeting notes
prompt = """
You are an AI meeting assistant.
Here is the transcript of a meeting:
---
{{{transcript}}}
---

Read the following meeting transcript and generate the output strictly in this format:

####
MoM
1. {Write the minutes of meeting in a numbered pointwise manner}
####
{If any other topics or action items are discussed, write them with the topic name as heading}
1. {pointwise content}
####
agenda
1. {List all agenda items in ascending order of dates, format: DD-MM-YYYY - Topic}
####

Rules:
- Start the entire response with "####" and end with "####".
- Do not include anything outside the given format.
- Keep numbering continuous under each section.
- If a section has no content, skip that section entirely (don’t leave it empty).
"""

response = model.generate_content(prompt)

print(response.text)
