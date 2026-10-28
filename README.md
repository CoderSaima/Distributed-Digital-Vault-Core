# The Distributed Digital Vault Core

A high-security, enterprise-grade file storage system built with **Django (Python)** and **PostgreSQL**. This application implements a **Zero-Disk In-Memory Cryptographic Pipeline** combined with Role-Based Access Control (RBAC). It ensures that files uploaded by users are mathematically scrambled before being saved, keeping them completely safe from hackers at rest and during transit.

---

## How It Works (The Security Architecture)

This project acts as a secure, blind vault for sensitive digital assets. Here is how your data is protected step-by-step:

1. **Role-Based Access Control (RBAC):** When a user attempts to upload a file, the backend verifies their email clearance. Only authorized roles (Managers) can trigger the encryption engine.
2. **In-Memory Mathematical Scrambling:** The moment a file stream enters the server from the user's PC, it is processed entirely in the RAM buffer. It uses **AES-256 (CFB Mode)** with a randomized 16-byte Initialization Vector (IV) to scramble the file data into an unreadable form. 
3. **Encrypted at Rest:** The raw file is *never* saved to the server's hard drive. Instead, the scrambled binary payload is committed directly to the database. Even if a hacker gains direct database access, the data is completely unreadable and useless to them.
4. **Encrypted in Transit:** When downloading, the scrambled payload is transferred through the network pipeline. If a hacker intercepts the network traffic, they only see scrambled bits.
5. **Safe Decryption on Demand:** Only when a valid, cryptographically signed token is provided, the backend pulls the binary data, decrypts it in memory using the server's secret key, and instantly streams it back to the authorized user's browser as a clean download.

---

## Features

- **No JavaScript Dependencies:** Built purely with Python and standard HTML/CSS forms to eliminate frontend security vulnerabilities (like token tampering).
- **Self-Destructing Download Links:** Generated secure download links utilize a cryptographic timestamp that completely expires and self-destructs after **10 minutes**.
- **Tamper Detection:** If anyone alters even a single character of the secure download URL token, Django's `Signer` catches it immediately and blocks the request with a **Tamper Alert**.

---

## How to Set Up and Run

### 1. Prerequisites
Make sure you have Python installed and your virtual environment activated:
```bash
# Activate your virtual environment (Windows)
venv\Scripts\activate
```

### 2. Install Cryptography Library
This project relies on the robust `cryptography` library for AES operations:
```bash
pip install cryptography
```

### 3. Sync the Database
Prepare your PostgreSQL database tables to store the encrypted binary fields:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Fire Up the Server
Start your local development server workspace:
```bash
python manage.py runserver
```

### 5. Access the Security Portal
Open your web browser and navigate directly to your interface endpoint address:
```text
http://127.0.0
```

---

## Core Project Components Included

- **`models.py`**: Defines the database schema utilizing `BinaryField` to house raw mathematical data arrays.
- **`crypto_utils.py`**: Handles the AES block generation, custom SHA-256 key hashing, IV splitting, and bit encryption/decryption loops.
- **`views.py`**: Orchestrates the RBAC checking, file buffer streaming, token signing, and link shelf-life tracking.
- **`upload.html`**: A clean, responsive dashboard allowing users to seamlessly interact with the cryptographic pipeline.
