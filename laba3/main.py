import random
import os
import string

from GammaEncryptionDictionary import GammaEncryptionDictionary
from GammaEncryptionAlgorithm import GammaEncryptionAlgorithm

def generate_random_text(length: int, alphabet: str) -> str:
    return ''.join(random.choice(alphabet) for _ in range(length))

def write_to_file(filename: str, text: str) -> None:
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(text)

def read_from_file(filename: str) -> str:
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()

def compare_files(file1: str, file2: str) -> bool:
    with open(file1, 'r', encoding='utf-8') as f1, open(file2, 'r', encoding='utf-8') as f2:
        return f1.read().strip() == f2.read().strip()

def main():
    all_ascii_bytes = bytes(range(256))
    alphabet = all_ascii_bytes.decode('cp1251', errors='replace')

    results_dir = "./"
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    original_file = os.path.join(results_dir, "original_text.txt")
    encrypted_file = os.path.join(results_dir, "encrypted_text.txt")
    decrypted_file = os.path.join(results_dir, "decrypted_text.txt")

    original_text = generate_random_text(100, alphabet)

    write_to_file(original_file, original_text)
    print(f"Сгенерирован случайный текст длиной {len(original_text)} символов и записан в {original_file}")
    A, B, C, t0 = 13, 256, 43, 37
    encryption_dictionary = GammaEncryptionDictionary(alphabet=alphabet)
    encryption_algorithm = GammaEncryptionAlgorithm(letter2index=encryption_dictionary.letter2index,index2letter=encryption_dictionary.index2letter,t0=t0,A=A,B=B, C=C)

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
    print(f"Исходный текст: {original_text[:36]}{'...' if len(original_text) > 36 else ''}")
    print(f"Зашифрованный: {encrypted_text[:36]}{'...' if len(encrypted_text) > 36 else ''}")
    print(f"Расшифрованный: {decrypted_text[:36]}{'...' if len(decrypted_text) > 36 else ''}")


if __name__ == "__main__":
    main()
