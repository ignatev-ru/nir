from flask import Flask, request, render_template, redirect, url_for
import random
import requests


app = Flask(__name__)

# Простейшая база данных пользователей (логин и пароль)
users = {
    'ignatev': 'Gv?z@AnXO6'
}

# Простейшая база данных для хранения отправленных одноразовых паролей
otp_database = {}

# Токен вашего бота Telegram
BOT_TOKEN = '7165651500:AAF9urxzV2ogpBbDE1WQXUfc5JzZxAe03LI'
# ID чата (ID пользователя, куда нужно отправить сообщение)
CHAT_ID = '300293512'

# Функция для генерации одноразового пароля
def generate_otp():
    return str(random.randint(1000, 9999))

# Отправка одноразового пароля в телеграм
def send_otp_telegram(otp, chat_id, bot_token):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    params = {
        "chat_id": chat_id,
        "text": f"Ваш одноразовый пароль: {otp}"
    }
    response = requests.post(url, params=params)
    if response.status_code != 200:
        print("Ошибка при отправке сообщения в телеграм:", response.text)
    else:
        print("Сообщение успешно отправлено в телеграм")

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if users.get(username) == password:
            otp = generate_otp()
            otp_database[username] = otp
            send_otp_telegram(otp, CHAT_ID, BOT_TOKEN)
            return redirect(url_for('enter_otp', username=username))
        else:
            return "Неверный логин или пароль"
    return render_template('login.html')

@app.route('/enter_otp', methods=['GET', 'POST'])
def enter_otp():
    username = request.args.get('username')
    if request.method == 'POST':
        otp = request.form['otp']
        stored_otp = otp_database.get(username)
        if stored_otp == otp:
            return "Одноразовый пароль верный. Доступ разрешен!"
        else:
            return "Неверный одноразовый пароль"
    else:
        return render_template('enter_otp.html')

if __name__ == '__main__':
    app.run(debug=True)
