import requests
import telebot
from db import insert_vacancies_to_db

def get_hh_vacancies(keyword, area_id):
    url = 'https://api.hh.ru/vacancies'
    params = {
        'text': keyword,
        'area': area_id,
        'per_page': 100
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        vacancies = []

        for vacancy in data.get('items', []):
            company = vacancy.get('employer', {}).get('name', 'Не указано')
            salary = vacancy.get('salary', 'Зарплата не указана')
            city = vacancy.get('area', {}).get('name', 'Не указан')
            url = vacancy.get('alternate_url', '#')

            vacancies.append({
                'company': company,
                'salary': salary,
                'city': city,
                'url': url
            })

        return vacancies
    else:
        print('Ошибка при получении данных:', response.status_code)
        return []

# Инициализация телеграм-бота
TOKEN = '6676268900:AAHUzBOtY46RyWw5XmSiI6A_qxZlAhZF_gI'
bot = telebot.TeleBot(TOKEN)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Отправь мне название вакансии, и я вышлю информацию о ней.")

# Обработчик для получения информации о вакансии
@bot.message_handler(func=lambda message: True)
def get_vacancy_info(message):
    # Разделение сообщения на параметры
    params = message.text.split(',')
    keyword = params[0].strip() if len(params) > 0 else None
    city = params[1].strip() if len(params) > 1 else None
    salary_range = params[2].strip() if len(params) > 2 else None

    # Получение вакансий и вставка в базу данных
    areas = {'Москва': 1, 'Санкт-Петербург': 2, 'Новосибирск': 4}
    area_id = areas.get(city)
    if keyword and area_id:
        vacancies = get_hh_vacancies(keyword, area_id)
        insert_vacancies_to_db(vacancies, keyword)



        # Отправка результатов пользователю
        if vacancies:
            for vacancy in vacancies:
                response_message = (
                    f"Компания: **{vacancy['company']}**\n"
                    f"Город: **{vacancy['city']}**\n"
                    f"Зарплата: **{vacancy['salary']}**\n"
                    f"Ссылка: {vacancy['url']}\n\n"
                )
                bot.send_message(message.chat.id, response_message, parse_mode='Markdown')
        else:
            bot.send_message(message.chat.id, "К сожалению, вакансий по вашему запросу не найдено.")


    # Запуск телеграм-бота
bot.polling()


# Запуск телеграм-бота
bot.polling()






