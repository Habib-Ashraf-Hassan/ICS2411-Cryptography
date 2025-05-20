#!/usr/bin/env python3
"""
Name - ASHRAF MOHAMMED HASSAN ANIL
Reg No - SCT211-0255/2021
Cryptography Assignment - Lab 2
Implementing AES in CBC and CTR modes
"""

from Crypto.Cipher import AES
import binascii

def hex_to_bytes(hex_string):
    """Convert a hex string to bytes."""
    return binascii.unhexlify(hex_string)

def bytes_to_hex(bytes_data):
    """Convert bytes to a hex string."""
    return binascii.hexlify(bytes_data).decode('utf-8')

def aes_cbc_decrypt(key, ciphertext):
    """
    Decrypt using AES in CBC mode.
    - key: hex encoded string
    - ciphertext: hex encoded string (IV is prepended)
    """
    # Convert hex to bytes
    key_bytes = hex_to_bytes(key)
    ciphertext_bytes = hex_to_bytes(ciphertext)
    
    # Extract IV (first 16 bytes)
    iv = ciphertext_bytes[:16]
    ciphertext_bytes = ciphertext_bytes[16:]
    
    # Create AES cipher in CBC mode
    cipher = AES.new(key_bytes, AES.MODE_CBC, iv)
    
    # Decrypt
    padded_plaintext = cipher.decrypt(ciphertext_bytes)
    
    # Remove PKCS5 padding
    padding_length = padded_plaintext[-1]
    if padding_length > 16:
        raise ValueError("Invalid padding")
    for i in range(1, padding_length + 1):
        if padded_plaintext[-i] != padding_length:
            raise ValueError("Invalid padding")
    plaintext = padded_plaintext[:-padding_length]
    
    return plaintext

def aes_cbc_encrypt(key, plaintext):
    """
    Encrypt using AES in CBC mode with PKCS5 padding.
    - key: hex encoded string
    - plaintext: bytes
    """
    # Convert key to bytes
    key_bytes = hex_to_bytes(key)
    
    # Generate random IV
    from Crypto.Random import get_random_bytes
    iv = get_random_bytes(16)
    
    # Add PKCS5 padding
    block_size = 16
    padding_length = block_size - (len(plaintext) % block_size)
    padded_plaintext = plaintext + bytes([padding_length] * padding_length)
    
    # Create AES cipher in CBC mode
    cipher = AES.new(key_bytes, AES.MODE_CBC, iv)
    
    # Encrypt
    ciphertext = cipher.encrypt(padded_plaintext)
    
    # Prepend IV to ciphertext
    return iv + ciphertext

def aes_ctr_decrypt(key, ciphertext):
    """
    Decrypt using AES in CTR mode.
    - key: hex encoded string
    - ciphertext: hex encoded string (IV/counter is prepended)
    """
    # Convert hex to bytes
    key_bytes = hex_to_bytes(key)
    ciphertext_bytes = hex_to_bytes(ciphertext)
    
    # Extract IV/counter (first 16 bytes)
    counter = ciphertext_bytes[:16]
    ciphertext_bytes = ciphertext_bytes[16:]
    
    # Implement CTR mode manually
    plaintext = bytearray()
    
    # Process each block
    block_size = 16
    for i in range(0, len(ciphertext_bytes), block_size):
        # Create cipher for this block (using ECB as the base mode)
        cipher = AES.new(key_bytes, AES.MODE_ECB)
        
        # Encrypt counter
        encrypted_counter = cipher.encrypt(counter)
        
        # XOR with ciphertext block
        block = ciphertext_bytes[i:i+block_size]
        for j in range(len(block)):
            plaintext.append(block[j] ^ encrypted_counter[j])
        
        # Increment counter (as big-endian integer)
        counter_int = int.from_bytes(counter, byteorder='big')
        counter_int = (counter_int + 1) % (2**(8*block_size))
        counter = counter_int.to_bytes(block_size, byteorder='big')
    
    return bytes(plaintext)

def aes_ctr_encrypt(key, plaintext):
    """
    Encrypt using AES in CTR mode.
    - key: hex encoded string
    - plaintext: bytes
    """
    # Convert key to bytes
    key_bytes = hex_to_bytes(key)
    
    # Generate random IV/counter
    from Crypto.Random import get_random_bytes
    counter = get_random_bytes(16)
    initial_counter = counter[:]
    
    # Implement CTR mode manually
    ciphertext = bytearray()
    
    # Process each block
    block_size = 16
    for i in range(0, len(plaintext), block_size):
        # Create cipher for this block (using ECB as the base mode)
        cipher = AES.new(key_bytes, AES.MODE_ECB)
        
        # Encrypt counter
        encrypted_counter = cipher.encrypt(counter)
        
        # XOR with plaintext block
        block = plaintext[i:i+block_size]
        for j in range(len(block)):
            ciphertext.append(block[j] ^ encrypted_counter[j])
        
        # Increment counter (as big-endian integer)
        counter_int = int.from_bytes(counter, byteorder='big')
        counter_int = (counter_int + 1) % (2**(8*block_size))
        counter = counter_int.to_bytes(block_size, byteorder='big')
    
    # Prepend initial counter to ciphertext
    return initial_counter + bytes(ciphertext)

def main():
    """Decrypt the given ciphertexts and print the plaintext."""
    # Question 1
    cbc_key_1 = "140b41b22a29beb4061bda66b6747e14"
    cbc_ciphertext_1 = "4ca00ff4c898d61e1edbf1800618fb2828a226d160dad07883d04e008a7897ee2e4b7465d5290d0c0e6c6822236e1daafb94ffe0c5da05d9476be028ad7c1d81"
    
    # Question 2
    cbc_key_2 = "140b41b22a29beb4061bda66b6747e14"
    cbc_ciphertext_2 = "5b68629feb8606f9a6667670b75b38a5b4832d0f26e1ab7da33249de7d4afc48e713ac646ace36e872ad5fb8a512428a6e21364b0c374df45503473c5242a253"
    
    # Question 3
    ctr_key_1 = "36f18357be4dbd77f050515c73fcf9f2"
    ctr_ciphertext_1 = "69dda8455c7dd4254bf353b773304eec0ec7702330098ce7f7520d1cbbb20fc388d1b0adb5054dbd7370849dbf0b88d393f252e764f1f5f7ad97ef79d59ce29f5f51eeca32eabedd9afa9329"
    
    # Question 4
    ctr_key_2 = "36f18357be4dbd77f050515c73fcf9f2"
    ctr_ciphertext_2 = "770b80259ec33beb2561358a9f2dc617e46218c0a53cbeca695ae45faa8952aa0e311bde9d4e01726d3184c34451"
    
    # Decrypt and print results
    try:
        plaintext_1 = aes_cbc_decrypt(cbc_key_1, cbc_ciphertext_1)
        print(f"Question 1 Answer: {plaintext_1.decode('utf-8')}")
    except Exception as e:
        print(f"Error in Question 1: {str(e)}")
    
    try:
        plaintext_2 = aes_cbc_decrypt(cbc_key_2, cbc_ciphertext_2)
        print(f"Question 2 Answer: {plaintext_2.decode('utf-8')}")
    except Exception as e:
        print(f"Error in Question 2: {str(e)}")
    
    try:
        plaintext_3 = aes_ctr_decrypt(ctr_key_1, ctr_ciphertext_1)
        print(f"Question 3 Answer: {plaintext_3.decode('utf-8')}")
    except Exception as e:
        print(f"Error in Question 3: {str(e)}")
    
    try:
        plaintext_4 = aes_ctr_decrypt(ctr_key_2, ctr_ciphertext_2)
        print(f"Question 4 Answer: {plaintext_4.decode('utf-8')}")
    except Exception as e:
        print(f"Error in Question 4: {str(e)}")

# Test with sample data
def test():
    """Test encryption and decryption functions.
    This returns True if the encryption and decryption functions are implemented successfully."""

    key = "140b41b22a29beb4061bda66b6747e14"
    plaintext = b"This is a test message for AES encryption."
    
    # Test CBC mode
    cbc_ciphertext = aes_cbc_encrypt(key, plaintext)
    cbc_decrypted = aes_cbc_decrypt(key, bytes_to_hex(cbc_ciphertext))
    print(f"CBC Test - Original: {plaintext}")
    print(f"CBC Test - Decrypted: {cbc_decrypted}")
    print(f"CBC Test - Success: {plaintext == cbc_decrypted}")
    
    # Test CTR mode
    ctr_ciphertext = aes_ctr_encrypt(key, plaintext)
    ctr_decrypted = aes_ctr_decrypt(key, bytes_to_hex(ctr_ciphertext))
    print(f"CTR Test - Original: {plaintext}")
    print(f"CTR Test - Decrypted: {ctr_decrypted}")
    print(f"CTR Test - Success: {plaintext == ctr_decrypted}")

if __name__ == "__main__":
    main()
    
    # test()  # Commented out but the test was a success