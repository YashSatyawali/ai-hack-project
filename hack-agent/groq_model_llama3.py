from groq import Groq
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv(dotenv_path=r'd:/RAJ/Python/project_test/ai-hack-project/.env')

api_key = os.getenv('GROQ_API_KEY')

client = Groq(api_key=api_key)

# Read transcript from file
with open(r'd:/RAJ/Python/project_test/ai-hack-project/whisper_test/2025-08-24_21-19-24_meeting_transcription.txt', 'r', encoding='utf-8') as f:
    transcript = f.read().strip()

#print(transcript)

# Prompt
prompt = f"""
You are an AI meeting assistant.
Here is the transcript of a meeting:
---
{transcript}
---

Read the following meeting transcript and generate the output strictly in this format:

####
MoM
1. {{Write the minutes of meeting in a numbered pointwise manner}}
####
{{If any other topics or action items are discussed, write them with the topic name as heading}}
1. {{pointwise content}}
####
agenda
1. {{List all agenda items in ascending order of dates, format: DD-MM-YYYY - Topic}}
####

Rules:
- Start the entire response with "####" and end with "####".
- Do not include anything outside the given format.
- Keep numbering continuous under each section.
- If a section has no content, skip that section entirely (don’t leave it empty).
"""

chat_completion = client.chat.completions.create(
    messages=[{"role": "user", "content": prompt}],
    model="llama-3.3-70b-versatile"
)

print(chat_completion.choices[0].message.content)
