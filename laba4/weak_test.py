from des import DES
from des_constants import IP, FP, E, S, P, PC1, PC2, LS
from BitString import BitString

weak_keys_hex = [
    "0101010101010101",
    "FEFEFEFEFEFEFEFE",
    "1F1F1F1F0E0E0E0E",
    "E0E0E0E0F1F1F1F1",
]

plaintext_str = "weak key test"

print(f"--- Демонстрация свойства слабых ключей DES ---")
print(f"Исходный текст: '{plaintext_str}' (длина: {len(plaintext_str)})")
print("-" * 50)

for key_hex in weak_keys_hex:
    des = DES(IP, FP, E, S, P, PC1, PC2, LS)

    print(f"--- Тестируем ключ: {key_hex} ---")
    intermediate_hex = des.encrypt_text(plaintext_str, key_hex)

    pad_from_first_encryption = des.pad

    print(f"Количество добавленных символов ('_'): {pad_from_first_encryption}")
    print(f"Промежуточный шифртекст (hex): {intermediate_hex}")

    key_bitstring = BitString.from_bits(bin(int(key_hex, 16))[2:].zfill(64))

    final_result_text_blocks = []
    for i in range(0, len(intermediate_hex), 16):
        chunk_hex = intermediate_hex[i:i+16]
        block_bitstring = BitString.from_bits(bin(int(chunk_hex, 16))[2:].zfill(64))

        re_encrypted_block = des.encrypt_block(block_bitstring, key_bitstring)

        final_result_text_blocks.append(re_encrypted_block.sync_text())

    final_text_with_padding = "".join(final_result_text_blocks)

    if pad_from_first_encryption > 0:
        recovered_text = final_text_with_padding[:-pad_from_first_encryption]
    else:
        recovered_text = final_text_with_padding

    print(f"Текст после второго шифрования: '{recovered_text}'")

    if recovered_text == plaintext_str:
        print("Свойство слабого ключа выполнено.")
    else:
        print("Результат не совпадает с исходным текстом.")
    print()
