from stego import TrailingSpacesStego

stego = TrailingSpacesStego()

container = """Первая строка текста
Вторая строка текста
Третья строка текста
Четвёртая строка текста
Пятая строка текста
Шестая строка текста
Седьмая строка текста
Восьмая строка текста
Девятая строка текста
Десятая строка текста
Одиннадцатая строка текста
Двенадцатая строка текста
Тринадцатая строка текста
Четырнадцатая строка текста
Пятнадцатая строка текста
Шестнадцатая строка текста
Семнадцатая строка текста
Восемнадцатая строка текста
Девятнадцатая строка текста
Двадцатая строка текста
Двадцать первая строка текста
Двадцать вторая строка текста
Двадцать третья строка текста
Двадцать четвёртая строка текста
Двадцать пятая строка текста
Двадцать шестая строка текста
Двадцать седьмая строка текста
Двадцать восьмая строка текста
Двадцать девятая строка текста
Тридцатая строка текста
Тридцать первая строка текста
Тридцать вторая строка текста
Тридцать третья строка текста
Тридцать четвёртая строка текста
Тридцать пятая строка текста
Тридцать шестая строка текста
Тридцать седьмая строка текста
Тридцать восьмая строка текста
Тридцать девятая строка текста
Сороковая строка текста
Сорок первая строка текста
Сорок вторая строка текста
Сорок третья строка текста
Сорок четвёртая строка текста
Сорок пятая строка текста
Сорок шестая строка текста
Сорок седьмая строка текста
Сорок восьмая строка текста
Последняя строка"""

secret = "Test"


print("="*60)
print("РЕЖИМ 1: Один/два пробела в конце строки")
print("="*60)


print("\n--- 1.1. Открытый контейнер ---\n")

preprocessed = stego.preprocess_container(container)
print("Открытый контейнер (первые 5 строк):")
for line in preprocessed.split('\n')[:5]:
    print(f"  '{line}'")
print("  ...")

capacity = stego.get_capacity_mode1(preprocessed)
print(f"\nКоличество строк: {len(preprocessed.split(chr(10)))}")
print(f"Ёмкость контейнера: {capacity} бит ({capacity // 8} байт)")


print("\n--- 1.2. Скрываемое сообщение и маркер ---\n")

print(f"Скрываемое сообщение: '{secret}'")
print(f"Маркер окончания: '\\x00' (NULL)")

message_bits = stego.text_to_bits(secret)
marker_bits = stego.text_to_bits('\x00')

print(f"\nБиты сообщения: {message_bits}")
print(f"Биты маркера:   {marker_bits}")
print(f"Полная строка:  {message_bits + marker_bits}")
print(f"Длина: {len(message_bits) + len(marker_bits)} бит")


print("\n--- 1.3. Встраивание сообщения ---\n")

stego_container = stego.embed_mode1(container, secret)

print("Заполненный контейнер (первые 5 строк):")
for i, line in enumerate(stego_container.split('\n')[:5]):
    trailing = len(line) - len(line.rstrip())
    print(f"  '{line}' ({trailing} пробел(а))")


print("\n--- 1.4. Извлечение сообщения ---\n")

extracted = stego.extract_mode1(stego_container)

print(f"Извлечённое сообщение: '{extracted}'")

if extracted == secret:
    print("Сообщения совпадают.")


print("\n" + "="*60)
print("РЕЖИМ 2: Обычный/неразрывный пробел")
print("="*60)


print("\n--- 2.1. Анализ контейнера ---\n")

bits_per_line = 8
capacity2 = stego.get_capacity_mode2(preprocessed, bits_per_line)
print(f"Бит на строку: {bits_per_line}")
print(f"Ёмкость контейнера: {capacity2} бит ({capacity2 // 8} байт)")


print("\n--- 2.2. Встраивание сообщения ---\n")

stego_container2 = stego.embed_mode2(container, secret, bits_per_line)

print("Заполненный контейнер (первые 5 строк):")
for i, line in enumerate(stego_container2.split('\n')[:5]):
    line_stripped = line.rstrip()
    trailing = line[len(line_stripped):]
    trailing_repr = trailing.replace(' ', 'S').replace('\xa0', 'N')
    print(f"  '{line_stripped}' + [{trailing_repr}]")

print("\n  S = обычный пробел (0x20), N = неразрывный пробел (0xA0)")


print("\n--- 2.3. Извлечение сообщения ---\n")

extracted2 = stego.extract_mode2(stego_container2, bits_per_line)

print(f"Извлечённое сообщение: '{extracted2}'")

if extracted2 == secret:
    print("Сообщения совпадают.")
