from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.llm import generate_terraform, fix_terraform, explain_terraform, fix_terraform_with_error
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




MAX_RETRIES = 3

@app.get("/generate")
def generate(prompt: str):
    raw_output = generate_terraform(prompt)

    def parse_llm_output(raw: str):
        clean = raw.strip()
        if clean.startswith("```"):
            clean = clean.split("```")[1]
        try:
            return json.loads(clean), None
        except Exception:
            return None, "Invalid LLM output"

    data, err = parse_llm_output(raw_output)
    if err:
        print("RAW OUTPUT:", raw_output)
        return {"error": err}

    terraform_code = data.get("terraform", "")
    last_error = None

    for attempt in range(MAX_RETRIES):
        is_valid, message = validate_terraform(terraform_code)
        print(f"[Attempt {attempt + 1}] valid={is_valid} | {message}")  # add this

        if is_valid:
            with open("terraform_output/main.tf", "w") as f:
                f.write(terraform_code)
            return {
                "terraform": terraform_code,
                "explanation": data.get("explanation"),
                "validation": message,
                "attempts": attempt + 1,
            }

        last_error = message
        if attempt < MAX_RETRIES - 1:
            # Feed the error back to the LLM and retry
            raw_fixed = fix_terraform_with_error(terraform_code, last_error)
            fixed_data, err = parse_llm_output(raw_fixed)
            if err or not fixed_data:
                break
            terraform_code = fixed_data.get("terraform", terraform_code)

    return {
        "error": f"Validation failed after {MAX_RETRIES} attempts. Last error: {last_error}"
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