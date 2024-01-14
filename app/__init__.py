from passlib.context import CryptContext

ALGORITHM = "HS256"
JWT_ACCESS_SECRETY_KEY = "5b5a2c2d7f927f616d09a6b15a009b769dd5ac23f6498391c4d791a6a1c259db"
JWT_REFRESH_SECRET_KEY = "4b993043cbe3917d9eb77ec66451d8cf926df25f5c5b36a4597c599acca94427"

ALGORITHM = "argon2"
ACCESS_TOKEN_EXPIRE_MINUTES = 20  # 30 minutes
REFRESH_TOKEN_EXPIRE_DAYS = 7 # 7 days

bcrypt_context = CryptContext(schemes=["argon2"], deprecated='auto')