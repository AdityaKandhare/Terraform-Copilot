import subprocess
import tempfile
import os
import shutil

def validate_terraform(terraform_code: str) -> tuple[bool, str]:
    """
    Writes code to a temp dir, runs terraform init + validate.
    Returns (is_valid, message).
    """
    tmpdir = tempfile.mkdtemp()
    try:
        tf_path = os.path.join(tmpdir, "main.tf")
        with open(tf_path, "w") as f:
            f.write(terraform_code)

        init_result = subprocess.run(
            ["terraform", "init", "-input=false", "-no-color"],
            cwd=tmpdir,
            capture_output=True,
            text=True,
            timeout=60,
        )
        if init_result.returncode != 0:
            return False, f"terraform init failed:\n{init_result.stderr}"

        validate_result = subprocess.run(
            ["terraform", "validate", "-no-color"],
            cwd=tmpdir,
            capture_output=True,
            text=True,
            timeout=30,
        )
        if validate_result.returncode != 0:
            return False, validate_result.stdout or validate_result.stderr

        return True, "Validation passed"

    except FileNotFoundError:
        # Terraform CLI not installed — fall back to heuristic check
        return _heuristic_validate(terraform_code)
    except subprocess.TimeoutExpired:
        return False, "terraform validation timed out"
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


def _heuristic_validate(terraform_code: str) -> tuple[bool, str]:
    if "resource" not in terraform_code:
        return False, "No resource block found"
    if "provider" not in terraform_code:
        return False, "Missing provider block"
    return True, "Heuristic check passed (terraform CLI not available)"