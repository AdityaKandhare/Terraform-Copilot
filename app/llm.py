import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def load_prompt(file_path):
    with open(file_path, "r") as f:
        return f.read()


def generate_terraform(user_prompt: str):
    system_prompt = load_prompt("app/prompts/generate_v1.txt")

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    return response["choices"][0]["message"]["content"]


def fix_terraform(code: str):
    system_prompt = load_prompt("app/prompts/fix_v1.txt")

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": code}
        ]
    )

    return response["choices"][0]["message"]["content"]


def explain_terraform(code: str):
    system_prompt = load_prompt("app/prompts/explain_v1.txt")

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": code}
        ]
    )

    return response["choices"][0]["message"]["content"]