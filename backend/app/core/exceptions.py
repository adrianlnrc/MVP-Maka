from fastapi import HTTPException, status

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Credenciais inválidas",
    headers={"WWW-Authenticate": "Bearer"},
)

forbidden_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Acesso negado",
)

not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Recurso não encontrado",
)

subscription_required_exception = HTTPException(
    status_code=status.HTTP_402_PAYMENT_REQUIRED,
    detail="Assinatura ativa necessária para acessar este conteúdo",
)
