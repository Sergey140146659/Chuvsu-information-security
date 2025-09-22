import random
import os

from PermutationEncryptionDictionary import PermutationEncryptionDictionary
from PermutationEncryptionAlgorithm import PermutationEncryptionAlgorithm

def generate_random_text(length: int) -> str:
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
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
    block_size = 18

    results_dir = "./"
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    original_file = os.path.join(results_dir, "original_text.txt")
    encrypted_file = os.path.join(results_dir, "encrypted_text.txt")
    decrypted_file = os.path.join(results_dir, "decrypted_text.txt")

    print("Создание перестановки...")
    permutation_dict = PermutationEncryptionDictionary(block_size)
    permutation = permutation_dict.create_permutation()

    dict_path = permutation_dict.save_to_json(os.path.join(results_dir, "permutation.json"))
    print(f"Перестановка сохранена в {dict_path}")

    text_length = block_size * random.randint(3, 5)
    original_text = generate_random_text(text_length)

    write_to_file(original_file, original_text)
    print(f"Сгенерирован случайный текст длиной {text_length} символов и записан в {original_file}")

    encryption_algorithm = PermutationEncryptionAlgorithm(
        permutation_dict.permutation,
        permutation_dict.inverse_permutation,
        block_size
    )

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

    print("\nПример шифрования по блокам:")
    blocks = encryption_algorithm.text_split(original_text)
    for i, block in enumerate(blocks[:2]):
        encrypted_block = encryption_algorithm.encrypt_block(block)
        print(f"Блок {i+1}: '{block}' -> '{encrypted_block}'")

if __name__ == "__main__":
    main()
