from des import DES
from des_constants import IP, FP, E, S, P, PC1, PC2, LS
from BitString import BitString

des = DES(IP, FP, E, S, P, PC1, PC2, LS)

standard_plaintext = "This is a secret message for standard DES test."
standard_key_hex   = "A1B2C3D4E5F6A7B8"

print(f"Исходный текст: '{standard_plaintext}'")
print(f"Ключ (hex):      {standard_key_hex}")
print("-" * 20)

ciphertext = des.encrypt_text(standard_plaintext, standard_key_hex)
print(f"Шифртекст (hex): {ciphertext}")
print(f"Было добавлено '{des.pad}' символов-заполнителей ('_').")
print("-" * 20)

recovered_plaintext = des.decrypt_text(ciphertext, standard_key_hex)
print(f"Расшифрованный текст: '{recovered_plaintext}'")
print("-" * 20)

if recovered_plaintext == standard_plaintext:
    print("Успех! Исходный и расшифрованный тексты совпадают.")
else:
    print("Ошибка! Тексты не совпадают.")
