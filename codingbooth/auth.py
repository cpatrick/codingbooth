from passlib.context import CryptContext

# Context for hashing passwords see:
# http://packages.python.org/passlib/new_app_quickstart.html
pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    default="pbkdf2_sha256",
    all__vary_rounds=0.1,
    pbkdf2_sha256__default_rounds=8000,
    )


def encode_password(password):
    """Encode the password"""
    return pwd_context.encrypt(password)


def check_password(password, hash):
    """Verify the password."""
    return pwd_context.verify(password, hash)
