import re

def is_valid_phone_number(phone_number):
    # Accepts +2547XXXXXXXX or 2547XXXXXXXX
    pattern = r"^\+?2547\d{8}$"
    return re.match(pattern, phone_number) is not None
