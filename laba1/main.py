import random
import os

from EncryptionDictionary import EncryptionDictionary
from EncryptionAlgorithm import EncryptionAlgorithm

def generate_random_text(alphabet: list, length: int) -> str:
    return ''.join(str(random.choice(alphabet)) for _ in range(length))

def write_to_file(filename: str, text: str) -> None:
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(text)

def read_from_file(filename: str) -> str:
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()

def compare_files(file1: str, file2: str) -> bool:
    with open(file1, 'r', encoding='utf-8') as f1, open(file2, 'r', encoding='utf-8') as f2:
        return f1.read() == f2.read()

def main():
    alphabet = [0, 1, 2, 3, 4]
    block_size = 2

    results_dir = "./"
    original_file = os.path.join(results_dir, "original_text.txt")
    encrypted_file = os.path.join(results_dir, "encrypted_text.txt")
    decrypted_file = os.path.join(results_dir, "decrypted_text.txt")

    print("Создание словаря шифрования...")
    encryption_dict = EncryptionDictionary(alphabet, block_size)
    dictionary = encryption_dict.create_dictionary()

    dict_path = encryption_dict.save_to_json(os.path.join(results_dir, "encryption_dict.json"))
    print(f"Словарь шифрования сохранен в {dict_path}")

    is_bijective = encryption_dict.is_bijective()
    print(f"Словарь биективный: {is_bijective}")

    text_length = block_size * random.randint(10, 20)
    original_text = generate_random_text(alphabet, text_length)

    write_to_file(original_file, original_text)
    print(f"Сгенерирован случайный текст длиной {text_length} символов и записан в {original_file}")

    encryption_algorithm = EncryptionAlgorithm(dictionary, block_size)

    encrypted_text = encryption_algorithm.encrypt_text(original_text)
    write_to_file(encrypted_file, encrypted_text)
    print(f"Текст зашифрован и записан в {encrypted_file}")

    decrypted_text = encryption_algorithm.decrypt_text(encrypted_text)
    write_to_file(decrypted_file, decrypted_text)
    print(f"Текст расшифрован и записан в {decrypted_file}")

    if compare_files(original_file, decrypted_file):
        print("Проверка пройдена: исходный и расшифрованный тексты совпадают.")
    else:
        print("Ошибка: исходный и расшифрованный тексты не совпадают!")

    print("\nПример:")
    print(f"Исходный текст: {original_text[:30]}{'...' if len(original_text) > 30 else ''}")
    print(f"Зашифрованный: {encrypted_text[:30]}{'...' if len(encrypted_text) > 30 else ''}")
    print(f"Расшифрованный: {decrypted_text[:30]}{'...' if len(decrypted_text) > 30 else ''}")

if __name__ == "__main__":
    main()
