import random
import string

class PasswordGenerator:
    def generate_password(self, length):
        characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(characters) for _ in range(length))

generator = PasswordGenerator()
password_length = int(input("Введите длину пароля: "))
print("Сгенерированный пароль:", generator.generate_password(password_length))
