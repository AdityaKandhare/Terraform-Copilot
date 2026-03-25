from fastapi import FastAPI
from app.llm import generate_terraform, fix_terraform
from app.evaluator import validate_terraform
import json
from app.llm import explain_terraform

app = FastAPI()


@app.get("/generate")
def generate(prompt: str):
    raw_output = generate_terraform(prompt)

    # 🔥 Clean LLM output
    clean_output = raw_output.strip()

    # remove markdown ```json ``` if present
    if clean_output.startswith("```"):
        clean_output = clean_output.split("```")[1]

    try:
        data = json.loads(clean_output)
    except Exception as e:
        print("RAW OUTPUT:", raw_output)
        return {"error": "Invalid LLM output"}

    # ✅ Validate Terraform
    is_valid, message = validate_terraform(data.get("terraform", {}))

    if not is_valid:
        return {"error": message}

    # ✅ Save formatted output
    with open("terraform_output/main.tf", "w") as f:
        f.write(data["terraform"])

    return {
        "terraform": data.get("terraform"),
        "explanation": data.get("explanation"),
        "validation": message
    }


@app.post("/fix")
def fix(code: str):
    raw_output = fix_terraform(code)

    # 🔥 Clean LLM output
    clean_output = raw_output.strip()

    if clean_output.startswith("```"):
        clean_output = clean_output.split("```")[1]

    try:
        data = json.loads(clean_output)
    except Exception as e:
        print("RAW OUTPUT:", raw_output)
        return {"error": "Invalid LLM output"}

    return data

@app.post("/explain")
def explain(code: str):
    raw_output = explain_terraform(code)

    clean_output = raw_output.strip()

    if clean_output.startswith("```"):
        clean_output = clean_output.split("```")[1]

    try:
        data = json.loads(clean_output)
    except:
        print("RAW OUTPUT:", raw_output)
        return {"error": "Invalid LLM output"}

    return data