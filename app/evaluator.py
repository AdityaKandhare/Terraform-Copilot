def validate_terraform(terraform_code: str):
    if "resource" not in terraform_code:
        return False, "No resource block found"

    if "provider" not in terraform_code:
        return False, "Missing provider block"

    return True, "Looks valid"