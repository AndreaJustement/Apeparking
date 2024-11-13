# encrypt_password.py

from app.security.security import get_password_hash

# Define la contraseña que quieres encriptar
plain_password = "admin"

# Usa la función de encriptación
hashed_password = get_password_hash(plain_password)

# Imprime la contraseña encriptada
print(f"Contraseña encriptada: {hashed_password}")
