from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

password = "shande123"

hashed = pwd_context.hash(password)
print("PASSWORD:", password)
print("HASH:", hashed)

print("VERIFIED:", pwd_context.verify("shande123", hashed))
