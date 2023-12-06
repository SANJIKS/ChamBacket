import qrcode

# Создаем объект QRCode
qr = qrcode.QRCode(
    version=1,  # Размер QR-кода (1-40)
    error_correction=qrcode.constants.ERROR_CORRECT_L,  # Уровень коррекции ошибок
    box_size=10,  # Размер каждой ячейки в пикселях
    border=4,  # Расстояние от края до QR-кода
)

# Устанавливаем данные для QR-кода
data = "Привет, это QR-код!"
qr.add_data(data)
qr.make(fit=True)

# Создаем изображение QR-кода
img = qr.make_image(fill_color="black", back_color="white")

# Сохраняем изображение
img.save("my_qrcode.png")
