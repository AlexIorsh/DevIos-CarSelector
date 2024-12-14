from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

# Создаем Flask-приложение
app = Flask(__name__)

# Папка для загрузки изображений
UPLOAD_FOLDER = 'static/photos'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Создать папку, если её нет

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/edit/<int:car_id>', methods=['GET', 'POST'])
def edit_car(car_id):
    conn = sqlite3.connect('autos.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        name = request.form.get('name')
        mark = request.form.get('mark')
        price = request.form.get('price')
        body = request.form.get('body')
        drive = request.form.get('drive')
        engine_power = request.form.get('engine_power')
        seats = request.form.get('seats')
        color = request.form.get('color')
        gearbox = request.form.get('gearbox')
        year = request.form.get('year')
        photo = request.files.get('photo')

        photo_filename = None
        if photo and photo.filename != '':
            photo_filename = photo.filename
            photo_path = os.path.join(app.config['UPLOAD_FOLDER'], photo_filename)
            photo.save(photo_path)

        cursor.execute('''
             UPDATE autos 
             SET name=?, mark=?, price=?, body=?, drive=?, engine_power=?, seats=?, color=?, gearbox=?, year=?, photo=?
             WHERE id_auto=?
         ''', (name, mark, price, body, drive, engine_power, seats, color, gearbox, year, photo_filename, car_id))
        conn.commit()
        conn.close()
        return redirect(url_for('catalog'))

    cursor.execute("SELECT * FROM autos WHERE id_auto=?", (car_id,))
    car = cursor.fetchone()
    conn.close()

    return render_template('edit_car.html', car=car)


@app.route('/delete/<int:car_id>', methods=['POST'])
def delete_car(car_id):
    try:
        conn = sqlite3.connect('autos.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM autos WHERE id_auto=?", (car_id,))
        conn.commit()
        conn.close()
        return redirect(url_for('catalog'))
    except Exception as e:
        print(f"Error deleting car: {e}")
        return "Ошибка при удалении автомобиля", 500


@app.route('/search', methods=['POST'])
def search():
    # Получаем данные из формы
    price_from = request.form['price_from']
    price_to = request.form['price_to']
    body = request.form['body']
    drive = request.form['drive']
    engine_power_from = request.form['engine_power_from']
    engine_power_to = request.form['engine_power_to']
    seats = request.form['seats']
    color = request.form['color']
    gearbox = request.form['gearbox']
    year_from = request.form['year_from']
    year_to = request.form['year_to']

    # Выводим полученные данные в консоль для проверки
    print(
        f"Received data: price from={price_from}, price to={price_to}, body={body}, drive={drive}, engine_power from={engine_power_from}, engine_power to={engine_power_to}, seats={seats}, color={color}, gearbox={gearbox}, year from={year_from}, year to={year_to}")

    try:
        # Подключаемся к базе данных
        conn = sqlite3.connect('autos.db')
        cursor = conn.cursor()

        # Строим запрос с фильтрацией по данным
        query = '''SELECT * FROM autos 
                   WHERE price BETWEEN ? AND ? 
                   AND body = ? 
                   AND drive = ? 
                   AND engine_power BETWEEN ? AND ? 
                   AND seats >= ? 
                   AND color = ? 
                   AND gearbox = ? 
                   AND year BETWEEN ? AND ?'''
        cursor.execute(query, (
        price_from, price_to, body, drive, engine_power_from, engine_power_to, seats, color, gearbox, year_from,
        year_to))

        # Извлекаем результаты
        cars = cursor.fetchall()
        conn.close()

        # Выводим результаты запроса в консоль для проверки
        print(f"Cars found: {cars}")

        # Возвращаем результаты на страницу
        return render_template('results.html', cars=cars)
    except Exception as e:
        print(f"Error: {e}")
        return render_template('results.html', cars=[])

@app.route('/add', methods=['GET', 'POST'])
def add_car():
    if request.method == 'POST':
        # Получение данных из формы
        name = request.form.get('name')
        mark = request.form.get('mark')
        price = request.form.get('price')
        body = request.form.get('body')
        drive = request.form.get('drive')
        engine_power = request.form.get('engine_power')
        seats = request.form.get('seats')
        color = request.form.get('color')
        gearbox = request.form.get('gearbox')
        year = request.form.get('year')

        # Обработка файла изображения
        photo = request.files.get('photo')
        photo_filename = None
        if photo and photo.filename != '':
            photo_filename = photo.filename
            photo_path = os.path.join(app.config['UPLOAD_FOLDER'], photo_filename)
            photo.save(photo_path)

        # Сохранение данных в базу данных
        try:
            conn = sqlite3.connect('autos.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO autos (name, mark, price, body, drive, engine_power, seats, color, gearbox, year, photo)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (name, mark, price, body, drive, engine_power, seats, color, gearbox, year, photo_filename))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))  # После добавления возвращаемся на главную
        except Exception as e:
            print(f"Error: {e}")
            return "Произошла ошибка при добавлении автомобиля", 500

    return render_template('add_car.html')
@app.route('/catalog')
def catalog():
    try:
        # Подключение к базе данных
        conn = sqlite3.connect('autos.db')
        cursor = conn.cursor()

        # Получение всех данных автомобилей
        cursor.execute("SELECT * FROM autos")
        cars = cursor.fetchall()
        conn.close()

        # Форматирование данных для передачи в шаблон
        formatted_cars = []
        for car in cars:
            formatted_cars.append({
                "name": car[1],
                "mark": car[2],
                "price": str(car[3]),  # Преобразование числа в строку
                "body": car[4],
                "drive": car[5],
                "region": car[6],
                "engine_power": str(car[7]),  # Преобразование числа в строку
                "seats": str(car[8]),  # Преобразование числа в строку
                "color": car[9],
                "gearbox": car[10],
                "year": str(car[11]),  # Преобразование числа в строку
                "photo": car[12]
            })

        # Передача данных в шаблон
        return render_template('catalog.html', cars=formatted_cars)
    except Exception as e:
        print(f"Error loading catalog: {e}")
        return "Ошибка при загрузке каталога.", 500

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store'
    return response

# Запуск приложения
if __name__ == '__main__':
    app.run(debug=True)
