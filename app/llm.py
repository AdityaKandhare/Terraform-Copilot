from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def load_prompt(file_path):
    with open(file_path, "r") as f:
        return f.read()


def generate_terraform(user_prompt: str):
    system_prompt = load_prompt("app/prompts/generate_v1.txt")

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    return response.choices[0].message.content


def fix_terraform(code: str):
    system_prompt = load_prompt("app/prompts/fix_v1.txt")

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": code}
        ]
    )

    return response.choices[0].message.content


def explain_terraform(code: str):
    system_prompt = load_prompt("app/prompts/explain_v1.txt")

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": code}
        ]
    )

    return response.choices[0].message.content

def fix_terraform_with_error(code: str, error: str) -> str:
    """Used by the validation retry loop in /generate."""
    system_prompt = load_prompt("app/prompts/fix_v1.txt")

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": (
                    f"The following Terraform code failed validation with this error:\n\n"
                    f"ERROR:\n{error}\n\n"
                    f"CODE:\n{code}\n\n"
                    f"Fix the code so it passes terraform validate."
                )
            }
        ]
    )
    return response.choices[0].message.content