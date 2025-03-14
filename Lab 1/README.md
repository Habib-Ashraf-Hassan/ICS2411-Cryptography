# Lab 1 - Many time pad
- Name: **Ashraf Mohammed Hassan Anil**
- Jomo Kenyatta University of Agriculture and technology B.sc Computer Science
- Reg No: **SCT211-0255/2021**

This repository contains a Python implementation in: _**many-time-pad.py**_ of a Many-Time Pad (MTP) attack, which exploits the vulnerability of reusing the same stream cipher key to encrypt multiple plaintexts. The goal of this exercise is to decrypt a target ciphertext by leveraging the properties of the XOR operation and the fact that the same key was reused across multiple ciphertexts.

---

## Table of Contents
1. [Introduction](#introduction)
2. [Background](#background)
3. [How the Attack Works](#how-the-attack-works)
4. [Step-by-Step Code Explanation](#step-by-step-explanation)
5. [Python Implementation](#python-implementation)
6. [Results](#results)
7. [Conclusion](#conclusion)

---

## Introduction

In this exercise, we are given **11 hex-encoded ciphertexts**, all encrypted using the same stream cipher key. The goal is to decrypt the **target ciphertext** (the 11th ciphertext) by exploiting the fact that the same key was reused. This is a classic example of a **Many-Time Pad (MTP) attack**, which is possible when a stream cipher key is reused across multiple plaintexts.

The Python script provided in this repository implements the attack and successfully decrypts most of the ciphertext, allowing us to guess the correct plaintext using basic English knowledge.

---

## Background

### Stream Ciphers and XOR
A **stream cipher** encrypts plaintext by combining it with a pseudorandom keystream (generated from a key) using the **XOR operation**. The encryption and decryption processes are identical:

```
Ciphertext = Plaintext XOR Keystream
Plaintext = Ciphertext XOR Keystream
```
If the same keystream is used to encrypt multiple plaintexts, an attacker can XOR the ciphertexts together to eliminate the keystream:
```
Ciphertext1 XOR Ciphertext2 = (Plaintext1 XOR Keystream) XOR (Plaintext2 XOR Keystream)
= Plaintext1 XOR Plaintext2
```

This reveals the XOR of the two plaintexts. If one of the plaintexts is known or can be guessed (e.g., it contains spaces or common English words), the other plaintext can be recovered.

---

## How the Attack Works

The attack leverages the following key insights:
1. **XOR Properties**:
   - XORing a space character (0x20) with an uppercase letter flips it to lowercase, and vice versa.
     eg:
     _'A' (0x41) ⊕ ' ' (0x20) = 'a' (0x61)_
     
     _'a' (0x61) ⊕ ' ' (0x20) = 'A' (0x41)_
   - XORing two letters produces a non-alphabetic character, which can help identify spaces.

2. **Guessing Spaces**:
   - If we guess that a particular position in one plaintext is a space, we can XOR the corresponding ciphertext with a space to recover the keystream byte at that position.
   - Using this keystream byte, we can decrypt the corresponding position in all other ciphertexts.

3. **Iterative Decryption**:
   - By iteratively guessing spaces and decrypting characters, we can gradually recover most of the plaintexts.

---

## Step-by-Step Explanation

### Step 1: Convert Hex Ciphertexts to Byte Arrays
Each ciphertext is a hex-encoded string. We first convert these hex strings into arrays of integers (bytes) for easier manipulation.

```python
def convert_to_array(hex_str):
    return [int(hex_str[i:i+2], 16) for i in range(0, len(hex_str), 2)]
```
### Step 2: Initialize Plaintext Arrays
We initialize arrays to store the decrypted plaintexts. Each position in the plaintext arrays is initially set to an underscore (_) as a placeholder.

```python
pt = [['_' for _ in range(len(ct))] for ct in cts_arrays]
```
### Step 3: XOR Ciphertexts and Guess Spaces

For each pair of ciphertexts, we XOR them together. If the result is a valid letter (A-Z or a-z), we assume that one of the plaintexts at that position is a space.
```python
for i in range(len(cts_arrays)):
    for j in range(len(cts_arrays)):
        if j == i:
            continue
        min_length = min(len(cts_arrays[i]), len(cts_arrays[j]))
        for k in range(min_length):
            x = cts_arrays[i][k] ^ cts_arrays[j][k]
            if (x >= ord('A') and x <= ord('Z')) or (x >= ord('a')) and x <= ord('z')):
                if check_all(i, cts_arrays[i][k], k, cts_arrays):
                    for l in range(len(pt))):
                        if k >= len(pt[l]) or pt[l][k] != '_':
                            continue
                        x = cts_arrays[i][k] ^ cts_arrays[l][k] ^ ord(' ')
                        if l == i or x == 0:
                            pt[l][k] = ' '
                        else:
                            pt[l][k] = chr(x)

```
### Step 4: Validate Guesses

The check_all function ensures that the guessed character is consistent across all ciphertexts. If the XOR result is not a valid letter, the guess is discarded.
```python

def check_all(arr_idx, ch, char_idx, cts_arrays):
    err_cnt = 0
    for j in range(len(cts_arrays)):
        if j == arr_idx or len(cts_arrays[j]) <= char_idx:
            continue
        x = ch ^ cts_arrays[j][char_idx]
        if x == 0:
            continue
        if not ((x >= ord('A') and x <= ord('Z')) or ((x >= ord('a')) and x <= ord('z'))):
            err_cnt += 1
            if err_cnt > 2:
                return False
    return True
```
### Step 5: Print Decrypted Plaintexts

Finally, we print the decrypted plaintexts. Most of the ciphertext will be decrypted, and the remaining gaps can be filled using basic English knowledge.
```python

for i in range(len(pt)):
    print(f"Plaintext {i+1}: {''.join(pt[i])}")
```
## Python Implementation

The full Python implementation found in the repository performs the following steps:
1. Converts hex-encoded ciphertexts into byte arrays.
2. Initializes plaintext arrays with placeholders.
3. XORs ciphertexts to guess spaces and decrypt characters.
4. Validates guesses and prints the decrypted plaintexts.

## Results
The script successfully decrypts most of the ciphertext, revealing the following plaintext for the target ciphertext

The code returns the decryption of all the ciphertext including the targetcipher text, from its output we can see the decryption returned is:

```
The secuet message is: Wh_n using a ~tream cipher, never use the key more than once
```

Which using our Knowledge in English we can decipher that the plain text was:

```
The secret message is: When using a stream cipher, never use the key more than once
```
## Conclusion

This exercise demonstrates the dangers of reusing a stream cipher key. By XORing ciphertexts encrypted with the same key, an attacker can recover the plaintexts without knowing the key. The Python script provided in this repository implements this attack and successfully decrypts the target ciphertext.
