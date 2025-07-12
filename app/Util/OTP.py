import random

def generate_OTP(length):
    return "".join(random.choices("0123456789",k=length))