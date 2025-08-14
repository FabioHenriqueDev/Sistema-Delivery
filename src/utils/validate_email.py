from email_validator import validate_email, EmailNotValidError

def validacao_email(email) -> bool:
    try:
        validate_email(email, check_deliverability=True)
    except EmailNotValidError:
        return False
    return True