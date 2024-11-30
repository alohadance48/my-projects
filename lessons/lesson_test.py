def caesar_cipher(text: str, shift: int) -> str:
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    translation_table = str.maketrans(
        alphabet,
        alphabet[shift:] + alphabet[:shift]  # Сдвигаем алфавит
    )
    return text.translate(translation_table)


def caesar_decipher(text: str, shift: int) -> str:
    return caesar_cipher(text, -shift)  # Для расшифровки просто меняем знак сдвига


def main():
    print("Добро пожаловать в игру Хакер!")
    message = input("Введите сообщение для шифрования: ").lower()  # Приводим к нижнему регистру
    shift = 3  # Устанавливаем фиксированный сдвиг, можно изменить по желанию
    encrypted_message = caesar_cipher(message, shift)

    print(f"\nЗашифрованное сообщение: {encrypted_message}")

    while True:
        choice = input("Хотите расшифровать сообщение? (да/нет): ").strip().lower()
        if choice == 'да':
            decrypted_message = caesar_decipher(encrypted_message, shift)
            print(f"Расшифрованное сообщение: {decrypted_message}")
            break
        elif choice == 'нет':
            print("Хорошо! Если захотите, возвращайтесь.")
            break
        else:
            print("Пожалуйста, введите 'да' или 'нет'.")


if __name__ == "__main__":
    main()
