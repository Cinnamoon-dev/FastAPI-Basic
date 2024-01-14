from passlib.context import CryptContext

ALGORITHM_TO_HASH = "HS512"
JWT_ACCESS_SECRETY_KEY = "5b5a2c2d7f927f616d09a6b15a009b769dd5ac23f6498391c4d791a6a1c259db"
JWT_REFRESH_SECRET_KEY = "4b993043cbe3917d9eb77ec66451d8cf926df25f5c5b36a4597c599acca94427"

ACCESS_TOKEN_EXPIRE_MINUTES = 20
REFRESH_TOKEN_EXPIRE_DAYS = 7 

bcrypt_context = CryptContext(schemes=["sha512_crypt"], deprecated='auto')