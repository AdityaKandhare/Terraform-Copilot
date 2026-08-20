# Terraform Copilot

Describe your infrastructure in plain English, get back working Terraform code.

It's a FastAPI app with a simple web UI. It uses GPT-4o to generate the code, then actually validates it with the Terraform CLI (`terraform init` + `terraform validate`) before returning it. If validation fails, the error is sent back to the model to fix, up to 3 times. So you only get code that passes validation.

## Features

- **Generate** - describe what you want, get Terraform code
- **Fix** - paste broken Terraform, get it fixed
- **Explain** - paste Terraform, get a plain-English explanation

## Setup

You need Python 3.10+, an OpenAI API key, and optionally the Terraform CLI (for real validation).

```bash
git clone https://github.com/AdityaKandhare/Terraform-Copilot.git
cd Terraform-Copilot

python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

echo "OPENAI_API_KEY=sk-..." > .env

uvicorn app.main:app --reload
```

Open http://localhost:8000 for the UI, or http://localhost:8000/docs for the API docs.

### Docker

The Docker image has Terraform installed, so validation always runs for real:

```bash
docker build -t terraform-copilot .
docker run -p 8000:8000 --env-file .env terraform-copilot
```

## API

| Method | Endpoint | Input |
|---|---|---|
| GET | `/generate?prompt=...` | Description of what you want |
| POST | `/fix` | `{"code": "..."}` |
| POST | `/explain` | `{"code": "..."}` |

Example:

```bash
curl "http://localhost:8000/generate?prompt=Create%20an%20S3%20bucket%20with%20versioning"
```

## Project structure

```
app/
├── main.py        # FastAPI endpoints + validate/retry loop
├── llm.py         # GPT-4o calls
├── evaluator.py   # Runs terraform init/validate in a temp dir
├── schemas.py     # Request models
└── prompts/       # System prompts
static/
└── ui.html        # Web UI (plain HTML/CSS/JS)
```

## Notes

- The tests hit the real OpenAI API, so running them needs a valid key.
- Generated code is saved to `terraform_output/main.tf`.
- If Terraform CLI isn't installed, it falls back to a basic syntax check.
