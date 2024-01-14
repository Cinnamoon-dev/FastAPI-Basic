from passlib.context import CryptContext

ALGORITHM = "HS256"
SECRETY_KEY = "TESTETESTE"

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated='auto')