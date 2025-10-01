from des import DES
from des_constants import IP, FP, E, S, P, PC1, PC2, LS
from BitString import BitString

des = DES(IP, FP, E, S, P, PC1, PC2, LS)

plaintext = "See how a single bit error corrupts the whole block!"
key_hex   = "FEDCBA9876543210"

print(f"Исходный текст: '{plaintext}'")
print(f"Ключ (hex):      {key_hex}\n")

original_ciphertext_hex = des.encrypt_text(plaintext, key_hex)
print(f"Оригинальный шифртекст (hex): {original_ciphertext_hex}")
print(f"Было добавлено '{des.pad}' символов-заполнителей ('_').\n")

original_bits = BitString.from_bits(bin(int(original_ciphertext_hex, 16))[2:].zfill(len(original_ciphertext_hex) * 4))

bit_to_flip_index = 20
print(f"Изменяем один бит в шифртексте по индексу: {bit_to_flip_index}")

modified_bits = original_bits.copy()
original_bit_value = modified_bits[bit_to_flip_index]
flipped_bit_value = '0' if original_bit_value == '1' else '1'
modified_bits[bit_to_flip_index] = flipped_bit_value

print(f"  > Значение бита было '{original_bit_value}', стало '{flipped_bit_value}'\n")

modified_ciphertext_hex = f"{int(modified_bits.bits, 2):0{len(original_ciphertext_hex)}X}"
print(f"Измененный шифртекст (hex):  {modified_ciphertext_hex}\n")


garbled_plaintext = des.decrypt_text(modified_ciphertext_hex, key_hex)
print(f"Результат дешифрования измененного текста:\n'{garbled_plaintext}'\n")
