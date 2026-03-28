from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.llm import generate_terraform, fix_terraform, explain_terraform
from app.evaluator import validate_terraform
from app.schemas import CodeInput
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def root():
    return FileResponse("static/ui.html")


@app.get("/generate")
def generate(prompt: str):
    raw_output = generate_terraform(prompt)

    clean_output = raw_output.strip()
    if clean_output.startswith("```"):
        clean_output = clean_output.split("```")[1]

    try:
        data = json.loads(clean_output)
    except Exception as e:
        print("RAW OUTPUT:", raw_output)
        return {"error": "Invalid LLM output"}

    is_valid, message = validate_terraform(data.get("terraform", {}))
    if not is_valid:
        return {"error": message}

    with open("terraform_output/main.tf", "w") as f:
        f.write(data["terraform"])

    return {
        "terraform": data.get("terraform"),
        "explanation": data.get("explanation"),
        "validation": message
    }


@app.post("/fix")
def fix(body: CodeInput):
    raw_output = fix_terraform(body.code)

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
def explain(body: CodeInput):
    raw_output = explain_terraform(body.code)

    clean_output = raw_output.strip()
    if clean_output.startswith("```"):
        clean_output = clean_output.split("```")[1]

    try:
        data = json.loads(clean_output)
    except:
        print("RAW OUTPUT:", raw_output)
        return {"error": "Invalid LLM output"}

    return data