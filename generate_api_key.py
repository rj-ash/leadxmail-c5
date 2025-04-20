import secrets
import string

def generate_api_key(length=32):
    """
    Generate a secure random API key.
    
    Args:
        length (int): Length of the API key. Default is 32 characters.
    
    Returns:
        str: A secure random API key
    """
    # Define the character set: letters (both cases), digits, and special characters
    alphabet = string.ascii_letters + string.digits + "_-"
    
    # Generate a random string of specified length
    api_key = ''.join(secrets.choice(alphabet) for _ in range(length))
    
    return api_key

if __name__ == "__main__":
    # Generate a new API key
    new_api_key = generate_api_key()
    print("\nGenerated API Key:", new_api_key)
    print("\nCopy this key and update it in your .env file:")
    print("API_KEY=" + new_api_key) 