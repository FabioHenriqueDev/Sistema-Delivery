def validate_senha(senha: str) -> bool:
    if len(senha) < 6:
        return False
    return True