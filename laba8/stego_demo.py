from stego import SentenceIntervalStego

stego = SentenceIntervalStego()

container = """Первое предложение. Второе предложение. Третье предложение.
Четвёртое предложение. Пятое предложение. Шестое предложение.
Седьмое предложение. Восьмое предложение. Девятое предложение.
Десятое предложение. Одиннадцатое. Двенадцатое. Тринадцатое.
Четырнадцатое. Пятнадцатое. Шестнадцатое. Семнадцатое.
Восемнадцатое. Девятнадцатое. Двадцатое. Двадцать первое.
Двадцать второе. Двадцать третье. Двадцать четвёртое.
Двадцать пятое. Двадцать шестое. Двадцать седьмое.
Двадцать восьмое. Двадцать девятое. Тридцатое.
Тридцать первое. Тридцать второе. Тридцать третье.
Тридцать четвёртое. Тридцать пятое. Тридцать шестое.
Тридцать седьмое. Тридцать восьмое. Тридцать девятое.
Сороковое. Сорок первое. Сорок второе. Сорок третье.
Сорок четвёртое. Сорок пятое. Сорок шестое. Сорок седьмое.
Сорок восьмое. Сорок девятое. Пятидесятое. """

secret = "Test"


print("="*60)
print("--- 1. Анализ контейнера ---")
print("="*60 + "\n")

print("Контейнер (фрагмент):")
print(container + "...")
print()

preprocessed = stego.preprocess_container(container)
capacity = stego.get_capacity(preprocessed)
print(f"Ёмкость контейнера: {capacity} бит ({capacity // 8} байт)")
print()


print("="*60)
print("--- 2. Скрываемое сообщение и маркер ---")
print("="*60 + "\n")

print(f"Скрываемое сообщение: '{secret}'")
print(f"Маркер окончания: '\\x00' (NULL)")

message_bits = stego.text_to_bits(secret)
marker_bits = stego.text_to_bits('\x00')

print(f"\nБиты сообщения: {message_bits}")
print(f"Биты маркера:   {marker_bits}")
print(f"Полная строка:  {message_bits + marker_bits}")
print(f"Длина: {len(message_bits) + len(marker_bits)} бит")
print()


print("="*60)
print("--- 3. Встраивание сообщения ---")
print("="*60 + "\n")

stego_container = stego.embed_with_marker(container, secret)

print("Заполненный контейнер (фрагмент):")
print(repr(stego_container))
print()


print("="*60)
print("--- 4. Извлечение сообщения ---")
print("="*60 + "\n")

extracted = stego.extract_with_marker(stego_container)

print(f"Извлечённое сообщение: '{extracted}'")

if extracted == secret:
    print("Сообщения совпадают.")
else:
    print("Сообщения не совпадают.")
