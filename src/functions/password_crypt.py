import bcrypt

def hash_password(password: str) -> bytes:
    """
    Hash a password for storing.
    """
    # Convert the password to bytes
    password_bytes = password.encode('utf-8')
    
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    
    return hashed_password

def verify_password(plain_password: str, hashed_password: bytes) -> bool:
    """
    Verify a stored password against one provided by user.
    """
    # Convert the plain_password to bytes
    password_bytes = plain_password.encode('utf-8')
    
    # Check if the plain_password matches the hashed_password
    return bcrypt.checkpw(password_bytes, hashed_password)

# # Example usage
# if __name__ == "__main__":
#     # Simulating password input
#     user_password = "mySecurePassword123"

#     # Hash the password
#     hashed = hash_password(user_password)
#     print(f"Hashed password: {hashed}")

#     # Verify the password
#     is_correct = verify_password(user_password, hashed)
#     print(f"Password is correct: {is_correct}")

#     # Try an incorrect password
#     wrong_password = "wrongPassword"
#     is_correct = verify_password(wrong_password, hashed)
#     print(f"Incorrect password is correct: {is_correct}")