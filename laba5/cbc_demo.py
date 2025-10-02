from des import DES
from des_constants import IP, FP, E, S, P, PC1, PC2, LS
from BitString import BitString


print("="*60)
print("--- 1. Демонстрация шифрования/дешифрования в режиме CBC ---")
print("="*60 + "\n")

des_cbc = DES(IP, FP, E, S, P, PC1, PC2, LS)
plaintext = "This is a simple test for the CBC mode implementation."
key_hex = "AABB09182736CCDD"

print(f"Исходный текст:         '{plaintext}'")
print(f"Ключ (hex):              {key_hex}\n")

ciphertext_with_iv = des_cbc.encrypt_text_cbc(plaintext, key_hex)

iv_from_ciphertext = ciphertext_with_iv[:16]
print(f"Случайный IV (hex):      {iv_from_ciphertext}")
print(f"Полный шифртекст (IV+C): {ciphertext_with_iv}\n")

recovered_text = des_cbc.decrypt_text_cbc(ciphertext_with_iv, key_hex)
print(f"Расшифрованный текст:    '{recovered_text}'")

if recovered_text == plaintext:
    print("\nИсходный и расшифрованный тексты совпадают.")
else:
    print("\nексты не совпадают.")


print("\n" + "="*60)
print("--- 2. Демонстрация распространения ошибки в режиме CBC ---")
print("="*60 + "\n")

bit_to_flip_index = 64 + 20
print(f"Изменяем один бит в первом блоке шифртекста (абсолютный индекс бита: {bit_to_flip_index})\n")

bits = BitString.from_bits(bin(int(ciphertext_with_iv, 16))[2:].zfill(len(ciphertext_with_iv) * 4))

bits[bit_to_flip_index] = '0' if bits[bit_to_flip_index] == '1' else '1'

modified_ciphertext_with_iv = f"{int(bits.bits, 2):0{len(ciphertext_with_iv)}X}"
print(f"Оригинальный шифртекст: {ciphertext_with_iv}")
print(f"Искаженный шифртекст:   {modified_ciphertext_with_iv}\n")

garbled_text = des_cbc.decrypt_text_cbc(modified_ciphertext_with_iv, key_hex)

print(f"Оригинальный текст: '{plaintext}'")
print(f"Искаженный текст:   '{garbled_text}'\n")

print("\n" + "="*60)
print("--- 3. Демонстрация шифрования идентичных блоков ---")
print("="*60 + "\n")


des_cbc_2 = DES(IP, FP, E, S, P, PC1, PC2, LS)

identical_blocks_text = "SameTextSameText"
print(f"Исходный текст: '{identical_blocks_text}' (содержит два блока 'SameText')")
print(f"Используем тот же ключ, но новый случайный IV.\n")

cipher_with_iv_2 = des_cbc_2.encrypt_text_cbc(identical_blocks_text, key_hex)

cipher_only = cipher_with_iv_2[16:]

cipher_block_1 = cipher_only[:16]
cipher_block_2 = cipher_only[16:]

print(f"Шифрблок 1 (hex): {cipher_block_1}")
print(f"Шифрблок 2 (hex): {cipher_block_2}\n")

if cipher_block_1 != cipher_block_2:
    print("Два идентичных блока открытого текста были зашифрованы в разные блоки шифртекста.")
else:
    print("Одинаковые блоки текста дали одинаковые блоки шифртекста")
