# email_bot.py

from groq import Groq
from dotenv import load_dotenv
import os
import json

# load_dotenv(dotenv_path="/Users/abhijit/Desktop/email_bot/.env")
client = Groq(api_key="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")

def extract_email_details(single_input):
    extraction_prompt = f"""
From the following message, extract and return only a JSON object with the following keys:
- sender
- recipient
- context
- tone
- instructions

Strictly return only the JSON object. Do not include any extra text or explanation.

Message:
\"\"\"{single_input}\"\"\"
"""
    extract_response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": extraction_prompt}],
        temperature=0.7,
        max_completion_tokens=512,
    )

    raw_content = extract_response.choices[0].message.content.strip()
    try:
        return json.loads(raw_content)
    except json.JSONDecodeError as e:
        raise ValueError(f"❌ LLM response is not valid JSON:\n{raw_content}") from e


def generate_email_from_input(single_input):
    extracted = extract_email_details(single_input)

    prompt = f"""
You are an expert business email writer. Write a professional email based on the following details.
Only output the email content — no headers, no explanations.

Sender Name: {extracted['sender']}
Recipient Name: {extracted['recipient']}
Context/Purpose of Email: {extracted['context']}
Tone: {extracted['tone']}
Additional Instructions: {extracted['instructions']}
"""

    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "system", "content": "You write clear, professional emails with appropriate tone."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_completion_tokens=1024,
    )

    return completion.choices[0].message.content.strip()
