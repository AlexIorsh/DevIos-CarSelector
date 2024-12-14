import sqlite3

# Подключение к базе данных
conn = sqlite3.connect('autos.db')
cursor = conn.cursor()

# Создание таблицы autos
cursor.execute('''
CREATE TABLE IF NOT EXISTS autos (
    id_auto INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    mark TEXT,
    price REAL,
    body TEXT,
    drive TEXT,
    region TEXT,
    engine_power INTEGER,
    seats INTEGER,
    color TEXT,
    gearbox TEXT,
    year INTEGER,
    photo TEXT
)
''')

# Добавление автомобилей в таблицу
cars = [
    ('Model 3', 'Tesla', 35000, 'Sedan', 'All-wheel', 'America', 283, 5, 'Red', 'Automatic', 2020, 'static/photos/model3.jpg'),
    ('Mustang', 'Ford', 45000, 'Coupe', 'Rear-wheel', 'America', 450, 2, 'Blue', 'Manual', 2021, 'static/photos/mustang.jpg'),
    ('Civic', 'Honda', 22000, 'Sedan', 'Front-wheel', 'Asia', 180, 5, 'Black', 'Automatic', 2022, 'static/photos/civic.jpg'),
    # Добавьте остальные автомобили
]

cursor.executemany('''
INSERT INTO autos (name, mark, price, body, drive, region, engine_power, seats, color, gearbox, year, photo) 
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
''', cars)

# Сохранение изменений и закрытие соединения
conn.commit()
conn.close()

print("Таблица 'autos' создана и данные добавлены.")
