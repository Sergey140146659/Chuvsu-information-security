from des import DES
from des_constants import IP, FP, E, S, P, PC1, PC2, LS
from BitString import BitString

des_cfb = DES(IP, FP, E, S, P, PC1, PC2, LS)


print("="*60)
print("--- 1. Демонстрация шифрования/дешифрования в режиме CFB ---")
print("="*60 + "\n")

plaintext = "CFB mode can encrypt text of any length, byte by byte."
key_hex = "1122334455667788"

print(f"Исходный текст:         '{plaintext}'")
print(f"Ключ (hex):              {key_hex}\n")

ciphertext_with_iv = des_cfb.encrypt_text_cfb(plaintext, key_hex)
iv_from_ciphertext = ciphertext_with_iv[:16]
print(f"Случайный IV (hex):      {iv_from_ciphertext}")
print(f"Полный шифртекст (IV+C): {ciphertext_with_iv}\n")

recovered_text = des_cfb.decrypt_text_cfb(ciphertext_with_iv, key_hex)
print(f"Расшифрованный текст:    '{recovered_text}'")

if recovered_text == plaintext:
    print("Исходный и расшифрованный тексты совпадают.")
else:
    print("Тексты не совпадают.")


print("\n" + "="*60)
print("--- 2. Демонстрация распространения ошибки в режиме CFB ---")
print("="*60 + "\n")


bit_to_flip_index = 16 * 4 + 20
print(f"Изменяем один бит в шифртексте (абсолютный индекс бита: {bit_to_flip_index})\n")

bits = BitString.from_bits(bin(int(ciphertext_with_iv, 16))[2:].zfill(len(ciphertext_with_iv) * 4))
bits[bit_to_flip_index] = '0' if bits[bit_to_flip_index] == '1' else '1'
modified_ciphertext_with_iv = f"{int(bits.bits, 2):0{len(ciphertext_with_iv)}X}"

garbled_text = des_cfb.decrypt_text_cfb(modified_ciphertext_with_iv, key_hex)

print(f"Оригинальный текст: '{plaintext}'")
print(f"Искаженный текст:   '{garbled_text}'\n")

print("\n" + "="*60)
print("--- 3. Демонстрация шифрования идентичных блоков ---")
print("="*60 + "\n")

identical_blocks_text = "SameTextSameText"
print(f"Исходный текст: '{identical_blocks_text}' (содержит два блока 'SameText')\n")

cipher_with_iv_2 = des_cfb.encrypt_text_cfb(identical_blocks_text, key_hex)
cipher_only_hex = cipher_with_iv_2[16:]

cipher_block_1 = cipher_only_hex[:16]
cipher_block_2 = cipher_only_hex[16:]

print(f"Шифрблок 1 (hex): {cipher_block_1}")
print(f"Шифрблок 2 (hex): {cipher_block_2}\n")

if cipher_block_1 != cipher_block_2:
    print("Два идентичных блока открытого текста были зашифрованы в РАЗНЫЕ блоки шифртекста.")
else:
    print("Режим CFB не скрыл повторение, что является ошибкой реализации.")
