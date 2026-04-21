from flask import Flask, render_template, request, jsonify, send_from_directory
from datetime import datetime
import requests

app = Flask(__name__)

# Telegram настройки
TELEGRAM_BOT_TOKEN = "8692751979:AAHywzCGI5f2q3PfhquI9CWp0JasjWaZBa8"
TELEGRAM_CHAT_ID = "449804614"

# ===== ПОЛНЫЕ ДАННЫЕ ПРАЙС-ЛИСТА =====
PRODUCTS = {
    # ========== ТРУБЫ НПВХ НАРУЖНЫЕ (РЫЖИЕ) SN2 ==========
    'pipes_npvh_outdoor_sn2': {
        'title': 'Трубы НПВХ наружные (рыжие) SN2 (2,0 мм)',
        'icon': 'fa-pipe-valve',
        'color': '#ff6b00',
        'image': 'pipe-red-110mm.jpg',
        'product_list': [
            {'name': 'Труба НПВХ 110 мм наружная SN2', 'spec': '2,0 мм', 'length': '0,25 м', 'pack': '10 шт'},
            {'name': 'Труба НПВХ 110 мм наружная SN2', 'spec': '2,0 мм', 'length': '0,5 м', 'pack': '10 шт'},
            {'name': 'Труба НПВХ 110 мм наружная SN2', 'spec': '2,0 мм', 'length': '1 м', 'pack': '6 шт'},
            {'name': 'Труба НПВХ 110 мм наружная SN2', 'spec': '2,0 мм', 'length': '1,5 м', 'pack': '6 шт'},
            {'name': 'Труба НПВХ 110 мм наружная SN2', 'spec': '2,0 мм', 'length': '2 м', 'pack': '6 шт'},
            {'name': 'Труба НПВХ 110 мм наружная SN2', 'spec': '2,0 мм', 'length': '3 м', 'pack': '6 шт'},
            {'name': 'Труба НПВХ 110 мм наружная SN2', 'spec': '2,0 мм', 'length': '4 м', 'pack': '6 шт'},
            {'name': 'Труба НПВХ 110 мм наружная SN2', 'spec': '2,0 мм', 'length': '5 м', 'pack': '6 шт'},
            {'name': 'Труба НПВХ 110 мм наружная SN2', 'spec': '2,0 мм', 'length': '6 м', 'pack': '6 шт'},
        ]
    },
    # ========== ТРУБЫ НПВХ НАРУЖНЫЕ (РЫЖИЕ) SN4 ==========
    'pipes_npvh_outdoor_sn4': {
        'title': 'Трубы НПВХ наружные (рыжие) SN4 (2,5 мм)',
        'icon': 'fa-pipe-valve',
        'color': '#ff6b00',
        'image': 'pipe-red-110mm.jpg',
        'product_list': [
            {'name': 'Труба НПВХ 110 мм наружная SN4', 'spec': '2,5 мм', 'length': '0,5 м', 'pack': '6 шт'},
            {'name': 'Труба НПВХ 110 мм наружная SN4', 'spec': '2,5 мм', 'length': '1 м', 'pack': '6 шт'},
            {'name': 'Труба НПВХ 110 мм наружная SN4', 'spec': '2,5 мм', 'length': '1,5 м', 'pack': '6 шт'},
            {'name': 'Труба НПВХ 110 мм наружная SN4', 'spec': '2,5 мм', 'length': '2 м', 'pack': '6 шт'},
            {'name': 'Труба НПВХ 110 мм наружная SN4', 'spec': '2,5 мм', 'length': '3 м', 'pack': '6 шт'},
            {'name': 'Труба НПВХ 110 мм наружная SN4', 'spec': '2,5 мм', 'length': '4 м', 'pack': '6 шт'},
            {'name': 'Труба НПВХ 110 мм наружная SN4', 'spec': '2,5 мм', 'length': '5 м', 'pack': '6 шт'},
            {'name': 'Труба НПВХ 110 мм наружная SN4', 'spec': '2,5 мм', 'length': '6 м', 'pack': '6 шт'},
        ]
    },
    # ========== ТРУБЫ НПВХ НАРУЖНЫЕ (РЫЖИЕ) SN8 ==========
    'pipes_npvh_outdoor_sn8': {
        'title': 'Трубы НПВХ наружные (рыжие) SN8 (3,2 мм)',
        'icon': 'fa-pipe-valve',
        'color': '#ff6b00',
        'image': 'pipe-red-110mm.jpg',
        'product_list': [
            {'name': 'Труба НПВХ 110 мм наружная SN8', 'spec': '3,2 мм', 'length': '0,25 м', 'pack': '10 шт'},
            {'name': 'Труба НПВХ 110 мм наружная SN8', 'spec': '3,2 мм', 'length': '0,5 м', 'pack': '6 шт'},
            {'name': 'Труба НПВХ 110 мм наружная SN8', 'spec': '3,2 мм', 'length': '1 м', 'pack': '6 шт'},
            {'name': 'Труба НПВХ 110 мм наружная SN8', 'spec': '3,2 мм', 'length': '1,5 м', 'pack': '6 шт'},
        ]
    },
    # ========== ТРУБЫ НПВХ НАРУЖНЫЕ 160 ММ ==========
    'pipes_npvh_outdoor_160': {
        'title': 'Трубы НПВХ наружные 160 мм (3,2 мм)',
        'icon': 'fa-pipe-valve',
        'color': '#ff6b00',
        'image': 'pipe-160mm.jpg',
        'product_list': [
            {'name': 'Труба НПВХ 160 мм наружная', 'spec': '3,2 мм', 'length': '0,5 м', 'pack': '4 шт'},
            {'name': 'Труба НПВХ 160 мм наружная', 'spec': '3,2 мм', 'length': '1 м', 'pack': '4 шт'},
            {'name': 'Труба НПВХ 160 мм наружная', 'spec': '3,2 мм', 'length': '1,5 м', 'pack': '4 шт'},
            {'name': 'Труба НПВХ 160 мм наружная', 'spec': '3,2 мм', 'length': '2 м', 'pack': '4 шт'},
            {'name': 'Труба НПВХ 160 мм наружная', 'spec': '3,2 мм', 'length': '3 м', 'pack': '4 шт'},
            {'name': 'Труба НПВХ 160 мм наружная', 'spec': '3,2 мм', 'length': '4 м', 'pack': '4 шт'},
            {'name': 'Труба НПВХ 160 мм наружная', 'spec': '3,2 мм', 'length': '5 м', 'pack': '4 шт'},
            {'name': 'Труба НПВХ 160 мм наружная', 'spec': '3,2 мм', 'length': '6 м', 'pack': '4 шт'},
        ]
    },
    # ========== ТРУБЫ НПВХ ВНУТРЕННИЕ (СЕРЫЕ) ==========
    'pipes_npvh_indoor': {
        'title': 'Трубы НПВХ внутренние (серые) 2,0 мм',
        'icon': 'fa-pipe-valve',
        'color': '#6c757d',
        'image': 'pipe-gray-110mm.jpg',
        'product_list': [
            {'name': 'Труба НПВХ 110 мм серая', 'spec': '2,0 мм', 'length': '0,25 м', 'pack': '10 шт'},
            {'name': 'Труба НПВХ 110 мм серая', 'spec': '2,0 мм', 'length': '0,5 м', 'pack': '6 шт'},
            {'name': 'Труба НПВХ 110 мм серая', 'spec': '2,0 мм', 'length': '1 м', 'pack': '6 шт'},
            {'name': 'Труба НПВХ 110 мм серая', 'spec': '2,0 мм', 'length': '1,5 м', 'pack': '6 шт'},
            {'name': 'Труба НПВХ 110 мм серая', 'spec': '2,0 мм', 'length': '2 м', 'pack': '6 шт'},
            {'name': 'Труба НПВХ 110 мм серая', 'spec': '2,0 мм', 'length': '3 м', 'pack': '6 шт'},
            {'name': 'Труба НПВХ 110 мм серая', 'spec': '2,0 мм', 'length': '4 м', 'pack': '6 шт'},
            {'name': 'Труба НПВХ 110 мм серая', 'spec': '2,0 мм', 'length': '5 м', 'pack': '6 шт'},
            {'name': 'Труба НПВХ 110 мм серая', 'spec': '2,0 мм', 'length': '6 м', 'pack': '6 шт'},
        ]
    },
    # ========== ФИТИНГИ ПП ==========
    'fittings_elbows_50': {
        'title': 'Отводы ПП 50 мм',
        'icon': 'fa-share-alt',
        'color': '#ff6b00',
        'image': 'fitting-elbow.jpg',
        'product_list': [
            {'name': 'Отвод ПП 50 мм', 'spec': '15°', 'pack': '100 шт'},
            {'name': 'Отвод ПП 50 мм', 'spec': '22°', 'pack': '100 шт'},
            {'name': 'Отвод ПП 50 мм', 'spec': '30°', 'pack': '100 шт'},
            {'name': 'Отвод ПП 50 мм', 'spec': '45°', 'pack': '100 шт'},
            {'name': 'Отвод ПП 50 мм', 'spec': '67°', 'pack': '100 шт'},
            {'name': 'Отвод ПП 50 мм', 'spec': '90°', 'pack': '100 шт'},
        ]
    },
    'fittings_elbows_110': {
        'title': 'Отводы ПП 110 мм',
        'icon': 'fa-share-alt',
        'color': '#ff6b00',
        'image': 'fitting-elbow-110.jpg',
        'product_list': [
            {'name': 'Отвод ПП 110 мм', 'spec': '15°', 'pack': '20 шт'},
            {'name': 'Отвод ПП 110 мм', 'spec': '30°', 'pack': '20 шт'},
            {'name': 'Отвод ПП 110 мм', 'spec': '45°', 'pack': '20 шт'},
            {'name': 'Отвод ПП 110 мм', 'spec': '67°', 'pack': '15 шт'},
            {'name': 'Отвод ПП 110 мм', 'spec': '90°', 'pack': '15 шт'},
        ]
    },
    'fittings_tees': {
        'title': 'Тройники ПП',
        'icon': 'fa-code-branch',
        'color': '#ff6b00',
        'image': 'fitting-tee.jpg',
        'product_list': [
            {'name': 'Тройник ПП 110/110/45°', 'spec': '110/110/45°', 'pack': '7 шт'},
            {'name': 'Тройник ПП 110/110/90°', 'spec': '110/110/90°', 'pack': '10 шт'},
            {'name': 'Тройник ПП 110/50/45°', 'spec': '110/50/45°', 'pack': '15 шт'},
            {'name': 'Тройник ПП 110/50/90°', 'spec': '110/50/90°', 'pack': '15 шт'},
        ]
    },
    'fittings_crosses': {
        'title': 'Крестовины ПП',
        'icon': 'fa-plus-square',
        'color': '#ff6b00',
        'image': 'fitting-cross.jpg',
        'product_list': [
            {'name': 'Крестовина ПП 110/110/110/45°', 'spec': '110/110/110/45°', 'pack': '6 шт'},
            {'name': 'Крестовина ПП 110/110/110/90°', 'spec': '110/110/110/90°', 'pack': '8 шт'},
            {'name': 'Крестовина ПП 110/110/50/90°', 'spec': '110/110/50/90°', 'pack': '8 шт'},
            {'name': 'Крестовина ПП 110/50/50/45°', 'spec': '110/50/50/45°', 'pack': '15 шт'},
            {'name': 'Крестовина ПП 110/50/50/90°', 'spec': '110/50/50/90°', 'pack': '15 шт'},
        ]
    },
    'fittings_couplings': {
        'title': 'Муфты и заглушки ПП',
        'icon': 'fa-link',
        'color': '#ff6b00',
        'image': 'fitting-coupling.jpg',
        'product_list': [
            {'name': 'Муфта ПП 110 мм', 'spec': '110 мм', 'pack': '25 шт'},
            {'name': 'Муфта ПП 32 мм', 'spec': '32 мм', 'pack': '300 шт'},
            {'name': 'Муфта ПП 40 мм', 'spec': '40 мм', 'pack': '80 шт'},
            {'name': 'Муфта ПП 50 мм', 'spec': '50 мм', 'pack': '100 шт'},
            {'name': 'Муфта наружная 110 мм', 'spec': 'наружная 110 мм', 'pack': '25 шт'},
            {'name': 'Заглушка ПП 110 мм', 'spec': '110 мм', 'pack': '100 шт'},
            {'name': 'Заглушка ПП 32 мм', 'spec': '32 мм', 'pack': '300 шт'},
            {'name': 'Заглушка ПП 40 мм', 'spec': '40 мм', 'pack': '200 шт'},
            {'name': 'Заглушка ПП 50 мм', 'spec': '50 мм', 'pack': '500 шт'},
            {'name': 'Заглушка наружная 110 мм', 'spec': 'наружная 110 мм', 'pack': '100 шт'},
        ]
    },
    'fittings_aerators': {
        'title': 'Аэраторы и зонты',
        'icon': 'fa-fan',
        'color': '#ff6b00',
        'image': 'fitting-aerator.jpg',
        'product_list': [
            {'name': 'Аэратор ПП 110 мм', 'spec': '110 мм', 'pack': '33 шт'},
            {'name': 'Аэратор ПП 50 мм', 'spec': '50 мм', 'pack': '100 шт'},
            {'name': 'Зонт ПП 110 мм разборный', 'spec': 'разборный', 'pack': '6 шт'},
            {'name': 'Зонт ПП 110 мм цельнолитой', 'spec': 'цельнолитой', 'pack': '50 шт'},
            {'name': 'Зонт ПП 110 мм наружный', 'spec': 'наружный', 'pack': '50 шт'},
            {'name': 'Зонт ПП 160 мм наружный', 'spec': 'наружный', 'pack': '24 шт'},
        ]
    },
    'fittings_traps': {
        'title': 'Трапы и клапаны',
        'icon': 'fa-water',
        'color': '#ff6b00',
        'image': 'fitting-trap.jpg',
        'product_list': [
            {'name': 'Трап прямой ПП 110 мм', 'spec': 'прямой', 'pack': '10 шт'},
            {'name': 'Трап прямой ПП 50 мм 10/10', 'spec': 'прямой 10/10', 'pack': '25 шт'},
            {'name': 'Трап прямой ПП 50 мм 15/15', 'spec': 'прямой 15/15', 'pack': '25 шт'},
            {'name': 'Трап угловой ПП 50 мм 10/10', 'spec': 'угловой 10/10', 'pack': '25 шт'},
            {'name': 'Трап угловой ПП 50 мм 15/15', 'spec': 'угловой 15/15', 'pack': '25 шт'},
            {'name': 'Обратный клапан ПП 50 мм', 'spec': '50 мм', 'pack': '1 шт'},
        ]
    },
    'fittings_clamps': {
        'title': 'Хомуты и переходы',
        'icon': 'fa-grip-vertical',
        'color': '#ff6b00',
        'image': 'fitting-clamp.jpg',
        'product_list': [
            {'name': 'Хомут ПП 160 мм', 'spec': '160 мм', 'pack': '50 шт'},
            {'name': 'Хомут ПП 50 мм', 'spec': '50 мм', 'pack': '100 шт'},
            {'name': 'Хомут эконом ПП 110 мм', 'spec': 'эконом 110 мм', 'pack': '100 шт'},
            {'name': 'Хомут эконом ПП 50 мм', 'spec': 'эконом 50 мм', 'pack': '100 шт'},
            {'name': 'Переход ПП 110-50 бутылка', 'spec': '110-50', 'pack': '50 шт'},
            {'name': 'Переход ПП 160-110 бутылка', 'spec': '160-110', 'pack': '16 шт'},
            {'name': 'Переход резиновый 110/124', 'spec': 'резиновый', 'pack': '100 шт'},
        ]
    },
    'fittings_cassettes': {
        'title': 'Кассеты ПП',
        'icon': 'fa-boxes',
        'color': '#ff6b00',
        'image': 'fitting-cassette.jpg',
        'product_list': [
            {'name': 'Кассета ПП 110 мм (10 мест)', 'spec': '10 мест', 'pack': '210 шт'},
            {'name': 'Кассета ПП 110 мм (6 мест)', 'spec': '6 мест', 'pack': '70 шт'},
            {'name': 'Кассета ПП 160 мм', 'spec': '160 мм', 'pack': '400 шт'},
            {'name': 'Кассета ПП 50 мм', 'spec': '50 мм', 'pack': '500 шт'},
        ]
    },
}

# Галерея
GALLERY = [
    {'image': 'pipe-red-110mm.jpg', 'title': 'Трубы НПВХ рыжие SN2, SN4, SN8'},
    {'image': 'pipe-gray-110mm.jpg', 'title': 'Трубы НПВХ серые для внутренней канализации'},
    {'image': 'fittings-1.jpg', 'title': 'Фитинги ПП: отводы, тройники, крестовины'},
]


def send_telegram(message):
    """Отправка сообщения в Telegram"""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {'chat_id': TELEGRAM_CHAT_ID, 'text': message, 'parse_mode': 'HTML'}
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        print(f"Telegram error: {e}")


@app.route('/')
def index():
    current_date = datetime.now().strftime("%d.%m.%Y")
    return render_template('index.html', products=PRODUCTS, gallery=GALLERY, current_date=current_date)


@app.route('/submit_lead', methods=['POST'])
def submit_lead():
    try:
        data = request.get_json()
        name = data.get('name', 'Не указано')
        phone = data.get('phone', 'Не указано')
        product = data.get('product', 'Не указано')
        quantity = data.get('quantity', '1')
        email = data.get('email', 'Не указан')
        comment = data.get('comment', 'Не указан')

        msg = f"""<b>📋 НОВАЯ ЗАЯВКА С САЙТА FLEXTRON</b>

👤 Имя: {name}
📞 Телефон: {phone}
📧 Email: {email}
🏭 Товар: {product}
📦 Количество: {quantity} шт
💬 Комментарий: {comment}
⏰ Время: {datetime.now().strftime('%H:%M %d.%m.%Y')}"""

        send_telegram(msg)
        print(f"✅ Заявка от {name}: {phone}")

        return jsonify({'success': True, 'message': 'Заявка отправлена!'})
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return jsonify({'success': True, 'message': 'Заявка принята!'})


@app.route('/health')
def health():
    return "OK", 200


@app.route('/robots.txt')
def robots():
    return send_from_directory('.', 'robots.txt')


@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory('.', 'sitemap.xml')


@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8000)