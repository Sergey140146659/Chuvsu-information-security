from des import DES
from des_constants import IP, FP, E, S, P, PC1, PC2, LS
from BitString import BitString

des_ofb = DES(IP, FP, E, S, P, PC1, PC2, LS)


print("="*60)
print("--- 1. Демонстрация шифрования/дешифрования в режиме OFB ---")
print("="*60 + "\n")

plaintext = "OFB mode is a synchronous stream cipher mode of operation."
key_hex = "1122334455667788"

print(f"Исходный текст:         '{plaintext}'")
print(f"Ключ (hex):              {key_hex}\n")

ciphertext_with_iv = des_ofb.encrypt_text_ofb(plaintext, key_hex)
iv_from_ciphertext = ciphertext_with_iv[:16]
print(f"Случайный IV (hex):      {iv_from_ciphertext}")
print(f"Полный шифртекст (IV+C): {ciphertext_with_iv}\n")

recovered_text = des_ofb.decrypt_text_ofb(ciphertext_with_iv, key_hex)
print(f"Расшифрованный текст:    '{recovered_text}'")

if recovered_text == plaintext:
    print("Исходный и расшифрованный тексты совпадают.")
else:
    print("Тексты не совпадают.")


print("\n" + "="*60)
print("--- 2. Демонстрация распространения ошибки в режиме OFB ---")
print("="*60 + "\n")

fixed_iv = "FEDCBA9876543210"
plaintext_err = "Test error propagation in OFB mode!"
ciphertext_with_iv = des_ofb.encrypt_text_ofb(plaintext_err, key_hex, fixed_iv)

bit_to_flip_index = 16 * 4 + 4
print(f"Изменяем один бит в шифртексте (индекс бита: {bit_to_flip_index})\n")

bits = BitString.from_bits(bin(int(ciphertext_with_iv, 16))[2:].zfill(len(ciphertext_with_iv) * 4))
bits[bit_to_flip_index] = '0' if bits[bit_to_flip_index] == '1' else '1'
modified_ciphertext_with_iv = f"{int(bits.bits, 2):0{len(ciphertext_with_iv)}X}"

garbled_text = des_ofb.decrypt_text_ofb(modified_ciphertext_with_iv, key_hex)

print(f"Оригинальный текст: '{plaintext_err}'")
print(f"Искаженный текст:   '{garbled_text}'")

diff_count = sum(1 for a, b in zip(plaintext_err, garbled_text) if a != b)
print(f"Количество искаженных символов: {diff_count}\n")


print("\n" + "="*60)
print("--- 3. Демонстрация шифрования идентичных блоков ---")
print("="*60 + "\n")

identical_blocks_text = "SameTextSameText"
print(f"Исходный текст: '{identical_blocks_text}' (содержит два блока 'SameText')\n")

cipher_with_iv_2 = des_ofb.encrypt_text_ofb(identical_blocks_text, key_hex)
cipher_only_hex = cipher_with_iv_2[16:]

cipher_block_1 = cipher_only_hex[:16]
cipher_block_2 = cipher_only_hex[16:]

print(f"Шифрблок 1 (hex): {cipher_block_1}")
print(f"Шифрблок 2 (hex): {cipher_block_2}\n")

if cipher_block_1 != cipher_block_2:
    print("Два идентичных блока открытого текста были зашифрованы в РАЗНЫЕ блоки шифртекста.")
else:
    print("Режим OFB не скрыл повторение, что является ошибкой реализации.")


print("\n" + "="*60)
print("--- 4. Демонстрация предварительной генерации гаммы ---")
print("="*60 + "\n")

fixed_iv_ks = "0123456789ABCDEF"
keystream = des_ofb.generate_keystream_ofb(key_hex, fixed_iv_ks, length=10)
print(f"Предварительно сгенерированная гамма: {keystream}")

test_text = "HelloWorld"
cipher = des_ofb.encrypt_text_ofb(test_text, key_hex, fixed_iv_ks)
cipher_only = cipher[16:]

cipher_bits = bin(int(cipher_only, 16))[2:].zfill(len(cipher_only) * 4)
plain_bits = ''.join(format(ord(c), '08b') for c in test_text)
recovered_keystream = ''.join('0' if a == b else '1' for a, b in zip(cipher_bits, plain_bits))

print(f"Гамма из C XOR P:                     {recovered_keystream}")

if keystream == recovered_keystream:
    print("Гаммы совпадают. Гамма не зависит от открытого текста.")
else:
    print("Гаммы не совпадают.")
