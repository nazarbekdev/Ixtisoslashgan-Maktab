import pandas as pd

# Jadval ma’lumotlarini tayyorlash
data = {
    "Savol": ["savol 1", "savol 2", "savol 3", "savol 4"],
    "Javob": ["mos javob", "mos javob", "mos javob", "mos javob"],
    "Xato javob 1": ["-", "xato javob", "-", "xato javob"],
    "Xato javob 2": ["-", "xato javob", "-", "xato javob"],
    "Xato javob 3": ["-", "xato javob", "-", "xato javob"],
    "Ball": [1.5, 2.8, 1.3, 1.8],
    "Savol darajasi": ["B", "Q", "Q", "B"],
    "Savol turi": ["ochiq", "yopiq", "ochiq", "yopiq"],
    "Variant": [1, 2, 2, 3]
}

# DataFrame yaratish
df = pd.DataFrame(data)

# Excel faylga saqlash
df.to_excel("test_file.xlsx", index=False)

print("Excel fayl 'test_file_holati.xlsx' sifatida saqlandi!")