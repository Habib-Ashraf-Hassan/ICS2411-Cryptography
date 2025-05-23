# Lab 2 - AES Encryption Modes

- Name: **Ashraf Mohammed Hassan Anil**
- **Jomo Kenyatta University of Agriculture and Technology**, B.Sc. Computer Science
- Reg No: **SCT211-0255/2021**

This repository contains a Python implementation in: _**lab2_solution.py**_ of AES encryption/decryption in both **CBC (Cipher Block Chaining)** and **CTR (Counter)** modes. The goal of this exercise is to decrypt given ciphertexts where the **IV (Initialization Vector)** is prepended to the ciphertext in both modes.

---

## Table of Contents

1. [Introduction](#introduction)
2. [Background](#background)

   - [Advanced Encryption Standard (AES)](#advanced-encryption-standard-aes)
   - [Cipher Block Chaining (CBC) Mode](#cipher-block-chaining-cbc-mode)
   - [Counter (CTR) Mode](#counter-ctr-mode)
   - [PKCS5 Padding](#pkcs5-padding)

3. [Implementation Details](#implementation-details)
4. [Code Explanation](#code-explanation)
5. [Results](#results)

---

## Introduction

In this lab, I implemented two AES encryption/decryption systems: AES in CBC mode and AES in CTR mode. For both implementations, the 16-byte Initialization Vector (IV) is randomly chosen and prepended to the ciphertext. In CBC mode, PKCS5 padding is used to ensure the plaintext is a multiple of the block size. The main task was to decrypt four ciphertexts (two for each mode) using the provided keys.

---

## Background

### Advanced Encryption Standard (AES)

AES is a symmetric block cipher that processes data in fixed-size blocks of 128 bits (16 bytes). It supports key sizes of 128, 192, and 256 bits. In this lab, we use 128-bit keys for encryption and decryption. Since AES operates on fixed-size blocks, we need to use a mode of operation to encrypt messages of arbitrary length.

### Cipher Block Chaining (CBC) Mode

In CBC mode, each plaintext block is XORed with the previous ciphertext block before being encrypted. This creates a chain where each ciphertext block depends on all previous plaintext blocks. For the first block, an Initialization Vector (IV) is used.

CBC encryption can be expressed as:

```bash
C[i] = Encrypt(P[i] ⊕ C[i-1])
```

and Decryption is the reverse:

```bash
P[i] = Decrypt(C[i]) ⊕ C[i-1]
```

### Counter (CTR) Mode

In CTR mode, the cipher is used to encrypt successive values of a counter, and the resulting stream is XORed with the plaintext to produce the ciphertext. The counter is initialized with the IV and incremented for each block.

With its encryption and decryption being as follows

```bash
C[i] = P[i] ⊕ Encrypt(IV + i)
P[i] = C[i] ⊕ Encrypt(IV + i)
```

CTR mode has the advantage of allowing random access to encrypted data blocks and does not require padding.

### PKCS5 Padding

PKCS5 padding ensures that the input data is a multiple of the block size. It works by adding N bytes of value N to the end of the data, where N is the number of padding bytes needed. If the data is already a multiple of the block size, a full block of padding is added.

---

## Implementation Details

## Libraries Used

- **Crypto.Cipher.AES**: For AES encryption/decryption
- **binascii**: For converting between hex strings and bytes

---

## AES-CBC Implementation

For **CBC mode**, the implementation includes:

- Extraction of the **IV** from the ciphertext
- Creation of the **AES cipher** using the key and IV
- **Decryption** of the ciphertext
- **Removal of PKCS5 padding** from the plaintext

---

## AES-CTR Implementation

For **CTR mode**, the implementation includes:

- Extraction of the **IV/counter** from the ciphertext
- **Manual implementation** of the CTR mode logic:

  For each block:

  - Encrypt the counter using **AES in ECB mode**
  - XOR the encrypted counter with the ciphertext block
  - Increment the counter

---

## Code Explanation

My `lab2_solution.py` file contains:

- Functions to handle AES encryption and decryption in CBC and CTR modes.
- Logic to extract the IV and apply the correct decryption.
- Sample decryption of four provided ciphertexts using their respective keys.

### The hex conversion function

```python
def hex_to_bytes(hex_string):
    """Convert a hex string to bytes."""
    return binascii.unhexlify(hex_string)

def bytes_to_hex(bytes_data):
    """Convert bytes to a hex string."""
    return binascii.hexlify(bytes_data).decode('utf-8')
```

### CBC Mode Decryption

```python
def aes_cbc_decrypt(key, ciphertext):
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
    plaintext = padded_plaintext[:-padding_length]

    return plaintext

```

This function:

- Converts the hex-encoded key and ciphertext to bytes
- Extracts the IV from the first 16 bytes of the ciphertext
- Creates an AES cipher in CBC mode with the key and IV
- Decrypts the ciphertext
- Removes the PKCS5 padding based on the value of the last byte

### My CTR mode decryption

```python
def aes_ctr_decrypt(key, ciphertext):
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
```

This could :

- Converts the hex-encoded key and ciphertext to bytes
- Extracts the IV/counter from the first 16 bytes of the ciphertext
  and for each block:

- Created an AES cipher in ECB mode (as a base for CTR)
- Encrypt the counter
- XOR the encrypted counter with the ciphertext block
- Increment the counter

## Results

The implementation successfully decrypted all four ciphertexts using their respective keys and IVs. The output plaintexts matched the expected results:

### CBC Mode

- **Question 1 (CBC)**:  
  _"Basic CBC mode encryption needs padding."_

- **Question 2 (CBC)**:  
  _"Our implementation uses rand. IV"_

---

### CTR Mode

- **Question 3 (CTR)**:  
  _"CTR mode lets you build a stream cipher from a block cipher."_

- **Question 4 (CTR)**:  
  _"Always avoid the two time pad!"_

---

These results validate the correctness of my implementations for both modes.
