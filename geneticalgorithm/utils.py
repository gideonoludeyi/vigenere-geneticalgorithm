def decrypt(key: str, cipher: str) -> str:
    """python implementation of decryption algorithm
    provided in Evaluation.java
    """
    # sanitize cipher text and key
    cipher = cipher.lower()
    cipher = cipher.replace(r"[^a-z]", "")
    cipher = cipher.replace(r"\s", "")
    cipher = [ord(c) for c in cipher]

    key = key.lower()
    key = key.replace(r"[^a-z]", "")
    key = key.replace(r"\s", "")
    key = [ord(c) - 97 for c in key]

    # decrypt each character
    plain = []
    key_ptr = 0
    for c in cipher:
        key_char = 0
        if len(key) > 0:
            # ignore any value not in the expected range
            while key[key_ptr] > 25 or key[key_ptr] < 0:
                key_ptr = (key_ptr + 1) % len(key)

            key_char = key[key_ptr]
            key_ptr = (key_ptr + 1) % len(key)

        plain.append(chr((26 + c - 97 - key_char) % 26 + 97))

    return "".join(i for i in plain)
