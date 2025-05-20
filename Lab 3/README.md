# Lab 3 - RSA Factorization and Decryption

**Name:** Ashraf Mohammed Hassan Anil  
**Institution:** Jomo Kenyatta University of Agriculture and Technology, B.Sc. Computer Science  
**Reg No:** SCT211-0255/2021

This repository contains a Python implementation in `lab3_solution.py` for factoring RSA moduli and decrypting RSA-encrypted messages. The implementation demonstrates how knowledge of approximate values of prime factors can be used to break RSA encryption.

---

## Table of Contents

- [Introduction](#introduction)
- [Background](#background)
- [Implementation Details](#implementation-details)
- [Mathematical Approach](#mathematical-approach)
- [Results](#results)
- [Conclusion](#conclusion)

---

## Introduction

In this lab, I implemented a technique to factor large RSA moduli where we have approximate knowledge of the prime factors. The assignment involved factoring three different RSA moduli and using the factorization of the first modulus to decrypt a ciphertext that was encrypted with RSA using PKCS v1.5 padding.

---

## Background

### RSA and the Vulnerability of Close Prime Factors

RSA security relies on the difficulty of factoring large numbers. The public key consists of a modulus `N` (product of two large primes `p` and `q`) and an encryption exponent `e`. The private key is the decryption exponent `d`, where:

```bash
e·d ≡ 1 (mod φ(N))
φ(N) = (p-1)(q-1)
```

However, if the prime factors are too close to each other, factorization becomes easier. This lab explores a simplified version of a factorization method that works when we have approximate values of the prime factors.

### PKCS v1.5 Padding

PKCS#1 v1.5 is a padding scheme for RSA encryption. In this scheme, the message is padded as follows:

1. Start with byte `0x02`
2. Add random non-zero bytes
3. Add a single `0x00` byte as a separator
4. Add the actual message bytes

After decryption, we need to locate the `0x00` separator and extract the message that follows it.

---

## Implementation Details

The implementation uses the `gmpy2` library for high-precision arithmetic and the `binascii` library for hex/ASCII conversion. The code solves four challenges:

1. Factoring the first RSA modulus
2. Factoring the second RSA modulus
3. Factoring the third RSA modulus (using a specialized approach)
4. Decrypting a ciphertext using the factorization from challenge 1

---

## Libraries Used

- `gmpy2`: For multi-precision arithmetic, modular inverses, etc.
- `binascii`: For converting between hex and binary data

---

## Mathematical Approach

### General Factorization Method

For the first two challenges, I use the following approach:

- Given `N = p·q`, where `p` and `q` are close to each other
- Let `A = (p + q) / 2` (the arithmetic mean of the factors)
- Let `B = (p - q) / 2`
- Then:

```bash
p = A + B
q = A - B
A² - B² = N → B = sqrt(A² - N)
```

- Estimate `A ≈ sqrt(N)` and refine as needed
- Once we have `A` and `B`, compute `p = A - B`, `q = A + B`

### Specialized Approach for Challenge 3

For the third challenge, I used a specialized method that leverages characteristics of the specific modulus:

1. Multiply `N` by 24 to get a value with factors having special properties
2. Find a value `a_` such that `(a_² - 24N)` is a perfect square
3. Calculate:

```bash
p = (a_ - sqrt(a_² - 24N)) / 6
q = N / p
```

### Decryption Process

For the decryption challenge:

1. Use the factors `p` and `q` from the first challenge
2. Calculate `φ(N) = (p - 1)(q - 1)`
3. Find the decryption exponent `d = e⁻¹ mod φ(N)`
4. Decrypt the ciphertext `c` by computing `m = c^d mod N`
5. Convert `m` to hex and parse the PKCS padding to extract the plaintext

---

## Results

### Challenge 1

```bash
p = 13407807929942597099574024998205846127479365820592393377723561443721764030073546976801874298166903427690031858186486050853753882811946569946433649006084171
q = 13407807929942597099574024998205846127479365820592393377723561443721764030073546976801874298166903427690031858186486050853753882811946569946433649006084097
```

### Challenge 2

```bash
p = 25464796146996183438008816563973942229341454268524157846328581927885777969985222835143851073249573454107384461557193173304497244814071505790566593206419759
q = 25464796146996183438008816563973942229341454268524157846328581927885777970106398054491246526970814167632563509541784734741871379856682354747718346471375403
```

### Challenge 3

```bash
p = 21909849592475533092273988531583955898982176093344929030099423584127212078126150044721102570957812665127475051465088833555993294644190955293613411658629209
q = 32864774388713299638410982797375933848473264140017393545149135376190818117189240035825816494954711821626076210364113848440012285863311027426121370050758081
```

#### Decryption Challenge

The decrypted plaintext from the challenge ciphertext is:

```bash
Factoring lets us break RSA
```

---

## Conclusion

This lab demonstrates a significant vulnerability in RSA when the prime factors are too close to each other. The factorization method used is a simplified version of more sophisticated techniques, but it clearly shows why RSA implementations need to ensure that the prime factors are sufficiently different from each other.

The successful decryption of the challenge ciphertext confirms the correctness of our factorization method and demonstrates the end-to-end process of breaking RSA when the factors can be determined.

### Key security takeaways:

- RSA prime factors should be generated to ensure they are not too close to each other
- Modern RSA implementations use much larger moduli (2048 bits or more) to mitigate factorization attacks
- Even with large moduli, proper prime generation procedures are essential
