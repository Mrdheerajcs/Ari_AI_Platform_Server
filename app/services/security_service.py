HIDDEN_FIELDS = [
    "password",
    "otp",
    "token",
    "salary",
    "bank_account",
    "aadhaar",
    "pan"
]


def mask_sensitive_data(text: str):

    if not text:
        return text

    lines = text.split("\n")

    safe_lines = []

    for line in lines:

        line_lower = line.lower()

        if any(field in line_lower for field in HIDDEN_FIELDS):
            safe_lines.append("[REDACTED]")
        else:
            safe_lines.append(line)

    return "\n".join(safe_lines)