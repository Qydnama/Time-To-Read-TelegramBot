import telebot
from bson import ObjectId
from telebot import types, TeleBot
from pymongo import MongoClient
import time
from datetime import datetime
import threading
import re
import requests
import random

MONGODB_URI = 'YOUR_MONGODB_URI'
TOKEN = "YOUR_TELEGRAMBOT_KEY"
GOOGLE_BOOKS_API = 'YOUR_TELEGRAM_BOOKS_KEY'

bot: TeleBot = telebot.TeleBot(TOKEN)
client = MongoClient(MONGODB_URI)
db = client.timeToReadBot
books_collection = db.books
users_collection = db.users


# ------------------------------------------------------------------------------------------------
@bot.message_handler(func=lambda message: message.text == "Помощь")
def text_help(message):
    helpFunc(message)


@bot.message_handler(commands=['help'])
def command_help(message):
    helpFunc(message)


def helpFunc(message):
    caption = "/start - Начать беседу с ботом\n/subscribe - Подписаться на рассылку\n/unsubscribe - Отписаться от " \
              "рассылки\n/books - Открыть вкладку с ботами\n/dailybook - Получить книгу дня\n/randombook - Получить " \
              "случайную книгу\n/search - Поиск книги по названию\n/about - Получить информацию о боте\n/help - " \
              "Вывезти все команды\n/back - Вернутся на главную вкладку "
    bot.send_message(message.chat.id, caption)


# ------------------------------------------------------------------------------------------------
@bot.message_handler(func=lambda message: message.text == "Начать")
def text_start(message):
    start(message)


@bot.message_handler(commands=['start'])
def command_start(message):
    start(message)


def start(message):
    print("Start Command Worked")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    item1 = types.KeyboardButton('Книги')
    item2 = types.KeyboardButton('О нас')
    markup.add(item1, item2)
    caption = "Привет! Я бот который поможет тебе читать больше книг. Выбери действие:"
    bot.send_message(message.chat.id, caption, reply_markup=markup)


# ------------------------------------------------------------------------------------------------
@bot.message_handler(func=lambda message: message.text == "О нас")
def text_about(message):
    handle_info(message)


@bot.message_handler(commands=['about'])
def command_about(message):
    handle_info(message)


def handle_info(message):
    bot.send_message(message.chat.id,
                     'Этот телеграм бот является частью научного исследования "Поддержка чтения среди казахстанской '
                     'молодежи в пространстве цифровых технологий".')


# ------------------------------------------------------------------------------------------------
@bot.message_handler(func=lambda message: message.text == "Книги")
def text_books(message):
    handle_books(message)


@bot.message_handler(commands=['books'])
def command_books(message):
    handle_books(message)


def handle_books(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    item1 = types.KeyboardButton('Книга дня')
    item2 = types.KeyboardButton('Случайная книга')
    item3 = types.KeyboardButton('Поиск книг по названию')
    item4 = types.KeyboardButton('Подписаться на рассылку')
    item5 = types.KeyboardButton('Отписаться от рассылки')
    item6 = types.KeyboardButton('Назад')
    markup.add(item1, item2, item3, item4, item5, item6)
    bot.send_message(message.chat.id, "Выбери действие:", reply_markup=markup)


# ------------------------------------------------------------------------------------------------
@bot.message_handler(func=lambda message: message.text == "Книга дня")
def text_daily_book(message):
    send_daily_book(message.chat.id)


@bot.message_handler(commands=['dailybook'])
def command_daily_book(message):
    send_daily_book(message.chat.id)


def send_daily_book(chat_id):
    book_of_the_day = books_collection.find_one({'book_of_the_day': True})

    if book_of_the_day:
        title = book_of_the_day.get('title', 'Название не указано')
        author = book_of_the_day.get('author', 'Автор не указан')
        description = book_of_the_day.get('description', 'Описание недоступно')
        link = book_of_the_day.get('link', 'Ссылка недоступна')
        image_link = book_of_the_day.get('image_link', None)

        message_text = f"📚 Книга дня 📚\nНазвание: {title}\nАвтор: {author}\nОписание: {description}\nСсылка: {link}"

        if image_link:
            if len(message_text) > 1024:
                print('1024')
                bot.send_photo(chat_id, image_link)
                bot.send_message(chat_id, message_text)
            else:
                bot.send_photo(chat_id, image_link, caption=message_text)
        else:
            bot.send_message(chat_id, message_text)
    else:
        bot.send_message(chat_id, "Книга дня еще не выбрана. Пожалуйста, попробуйте позже.")


# ------------------------------------------------------------------------------------------------
@bot.message_handler(func=lambda message: message.text == "Случайная книга")
def text_random_book(message):
    send_random_book(message.chat.id)


@bot.message_handler(commands=['randombook'])
def command_random_book(message):
    send_random_book(message.chat.id)


def send_random_book(message):
    books_list = [
        "Мастер и Маргарита - Михаил Булгаков",
        "Война и мир - Лев Толстой",
        "Преступление и наказание - Федор Достоевский",
        "Идиот - Федор Достоевский",
        "Братья Карамазовы - Федор Достоевский",
        "Анна Каренина - Лев Толстой",
        "Собачье сердце - Михаил Булгаков",
        "Евгений Онегин - Александр Пушкин",
        "Герой нашего времени - Михаил Лермонтов",
        "Обломов - Иван Гончаров",
        "Отцы и дети - Иван Тургенев",
        "Горе от ума - Александр Грибоедов",
        "Мертвые души - Николай Гоголь",
        "Ревизор - Николай Гоголь",
        "Вишневый сад - Антон Чехов",
        "Три сестры - Антон Чехов",
        "Чайка - Антон Чехов",
        "Доктор Живаго - Борис Пастернак",
        "Тихий Дон - Михаил Шолохов",
        "Андрей Рублев - Андрей Тарковский",
        "Солярис - Станислав Лем",
        "Пикник на обочине - Аркадий и Борис Стругацкие",
        "Трудно быть богом - Аркадий и Борис Стругацкие",
        "Понедельник начинается в субботу - Аркадий и Борис Стругацкие",
        "За миллиард лет до конца света - Аркадий и Борис Стругацкие",
        "Дети Арбата - Анатолий Рыбаков",
        "Жизнь и судьба - Василий Гроссман",
        "Белый пароход - Чингиз Айтматов",
        "Джамиля - Чингиз Айтматов",
        "Прощай, Гульсары! - Чингиз Айтматов",
        "12 стульев - Илья Ильф и Евгений Петров",
        "Золотой теленок - Илья Ильф и Евгений Петров",
        "Одиночество в сети - Януш Вишневский",
        "Москва и москвичи - Владимир Гиляровский",
        "Детство - Максим Горький",
        "В алых парусах - Александр Грин",
        "Алые паруса - Александр Грин",
        "Сказка о царе Салтане - Александр Пушкин",
        "Сказка о рыбаке и рыбке - Александр Пушкин",
        "Сказка о мертвой царевне и семи богатырях - Александр Пушкин",
        "Лолита - Владимир Набоков",
        "Дар - Владимир Набоков",
        "Палата №6 - Антон Чехов",
        "Степь - Антон Чехов",
        "Каштанка - Антон Чехов",
        "Черный монах - Антон Чехов",
        "Улисс - Джеймс Джойс",
        "Великий Гэтсби - Фрэнсис Скотт Фицджеральд",
        "1984 - Джордж Оруэлл",
        "О дивный новый мир - Олдос Хаксли",
        "Граф Монте-Кристо - Александр Дюма",
        "Три мушкетера - Александр Дюма",
        "Гамлет - Уильям Шекспир",
        "Ромео и Джульетта - Уильям Шекспир",
        "Макбет - Уильям Шекспир",
        "Гордость и предубеждение - Джейн Остен",
        "Джейн Эйр - Шарлотта Бронте",
        "Гроздья гнева - Джон Стейнбек",
        "Убить пересмешника - Харпер Ли",
        "В поисках утраченного времени - Марсель Пруст",
        "Алиса в Стране чудес - Льюис Кэрролл",
        "Повелитель мух - Уильям Голдинг",
        "Сто лет одиночества - Габриэль Гарсиа Маркес",
        "Лолита - Владимир Набоков",
        "Анна Каренина - Лев Толстой",
        "Война и мир - Лев Толстой",
        "Крестный отец - Марио Пьюзо",
        "Фауст - Иоганн Вольфганг фон Гёте",
        "Дон Кихот - Мигель де Сервантес",
        "Божественная комедия - Данте Алигьери",
        "Идиот - Федор Достоевский",
        "Моби Дик - Герман Мелвилл",
        "Франкенштейн - Мэри Шелли",
        "Дракула - Брэм Стокер",
        "1984 - Джордж Оруэлл",
        "Большие надежды - Чарльз Диккенс",
        "Оливер Твист - Чарльз Диккенс",
        "Рождественская песнь - Чарльз Диккенс",
        "Жестокий век - Кен Фоллет",
        "Столпы Земли - Кен Фоллет",
        "Унесенные ветром - Маргарет Митчелл",
        "Поймай ветер - Харуки Мураками",
        "Норвежский лес - Харуки Мураками",
        "Кафка на пляже - Харуки Мураками",
        "1Q84 - Харуки Мураками",
        "Игра престолов - Джордж Р. Р. Мартин",
        "Клан Сопрано - Дэвид Чейз",
        "Хроники Нарнии - К. С. Льюис",
        "Гарри Поттер - Дж. К. Роулинг",
        "Властелин колец - Дж. Р. Р. Толкиен",
        "Хоббит, или Туда и обратно - Дж. Р. Р. Толкиен",
        "Сильмариллион - Дж. Р. Р. Толкиен",
        "Песнь льда и пламени - Джордж Р. Р. Мартин"
    ]
    get_random_book(message, books_list)


def get_random_book(message, book_list):

    random_title = random.choice(book_list)
    url = 'https://www.googleapis.com/books/v1/volumes'
    params = {
        'q': f"{random_title}",
        'key': GOOGLE_BOOKS_API,
        'maxResults': 1,
        'langRestrict': 'ru',
        'filter': 'ebooks',
        'printType': 'books'
    }
    response = requests.get(url, params=params)
    print(response)
    if response.status_code == 200:
        print(response.json())
        books = response.json().get('items', [])
        if books:
            book = books[0]  # Берем первый результат поиска
            print(book)
            title = book['volumeInfo'].get('title', 'Название не найдено')
            authors = ', '.join(book['volumeInfo'].get('authors', ['Авторы не указаны']))
            description = book['volumeInfo'].get('description', 'Описание отсутствует')
            publishedDate = book['volumeInfo'].get('publishedDate', 'Дата выпуска не указана')
            categories = ', '.join(book['volumeInfo'].get('categories', ['Жанры не указаны']))
            link = book['volumeInfo'].get('previewLink', 'Ссылка не доступна')
            image_link = book['volumeInfo'].get('imageLinks', {}).get('thumbnail', '')

            message_text = f"Название: {title}\nАвторы: {authors}\nОписание: {description}\nГод выпуска: {publishedDate}\nЖанры: {categories}\nСсылка: {link}"
            if image_link:
                if len(message_text) > 1024:
                    bot.send_photo(message, image_link)
                    bot.send_message(message, message_text)
                else:
                    bot.send_photo(message, image_link, caption=message_text)
            else:
                bot.send_message(message, message_text)
        else:
            return "Книги по вашему запросу не найдены."
    else:
        return "Произошла ошибка при поиске рандомной книги."


# ------------------------------------------------------------------------------------------------
@bot.message_handler(func=lambda message: message.text.startswith("Поиск книг по названию"))
def text_search(message):
    msg = bot.reply_to(message, "Введите название книги для поиска:")
    bot.register_next_step_handler(msg, perform_book_search)


@bot.message_handler(commands=['search'])
def command_search(message):
    msg = bot.reply_to(message, "Введите название книги для поиска:")
    bot.register_next_step_handler(msg, perform_book_search)


def perform_book_search(message):
    keyword = message.text
    search_book(message, keyword)


def search_book(message, keyword):
    url = 'https://www.googleapis.com/books/v1/volumes'
    params = {
        'q': f"+intitle:{keyword}",
        'key': GOOGLE_BOOKS_API,
        'maxResults': 1,
        'filter': 'ebooks',
        'printType': 'books'
    }
    response = requests.get(url, params=params)
    print(response)
    if response.status_code == 200:
        print(response.json())
        books = response.json().get('items', [])
        if books:
            book = books[0]
            print(book)
            title = book['volumeInfo'].get('title', 'Название не найдено')
            authors = ', '.join(book['volumeInfo'].get('authors', ['Авторы не указаны']))
            description = book['volumeInfo'].get('description', 'Описание отсутствует')
            publishedDate = book['volumeInfo'].get('publishedDate', 'Дата выпуска не указана')
            categories = ', '.join(book['volumeInfo'].get('categories', ['Жанры не указаны']))
            link = book['volumeInfo'].get('previewLink', 'Ссылка не доступна')
            image_link = book['volumeInfo'].get('imageLinks', {}).get('thumbnail', '')

            message_text = f"Название: {title}\nАвторы: {authors}\nОписание: {description}\nГод выпуска: {publishedDate}\nЖанры: {categories}\nСсылка: {link}"
            if image_link:
                if len(message_text) > 1024:
                    bot.send_photo(message.chat.id, image_link)
                    bot.send_message(message.chat.id, message_text)
                else:
                    bot.send_photo(message.chat.id, image_link, caption=message_text)
            else:
                bot.send_message(message.chat.id, message_text)
        else:
            bot.reply_to(message, "Книги по вашему запросу не найдены.")
    else:
        bot.reply_to(message, "Произошла ошибка при запросе к Google Books API.")


# ------------------------------------------------------------------------------------------------
@bot.message_handler(func=lambda message: message.text == "Подписаться на рассылку")
def text_subscribe(message):
    subscribe(message)


@bot.message_handler(commands=['subscribe'])
def command_subscribe(message):
    subscribe(message)


def subscribe(message):
    user_id = message.chat.id
    existing_user = users_collection.find_one({'chat_id': user_id})
    if existing_user:
        current_time = existing_user.get('reminder_time', 'Не установлено')
        formatted_time = format_time(current_time)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        yes_button = types.KeyboardButton("Да")
        no_button = types.KeyboardButton("Нет")
        markup.add(yes_button, no_button)
        sent_message = bot.send_message(user_id,
                                        f"Вы уже подписаны на уведомления. Ваше текущее время уведомлений: {formatted_time}. Хотите поменять время?",
                                        reply_markup=markup)
        bot.register_next_step_handler(sent_message, process_time_change_decision)
    else:
        msg = bot.send_message(user_id,
                               "В какое время вы хотите получать уведомления? Укажите время в формате ЧЧ:ММ ("
                               "24-часовой формат).")
        bot.register_next_step_handler(msg, process_subscription_time)


def format_time(minutes_since_midnight):
    if minutes_since_midnight == "Не установлено":
        return minutes_since_midnight

    hours, minutes = divmod(int(minutes_since_midnight), 60)
    return f"{hours:02d}:{minutes:02d}"


def process_time_change_decision(message):
    if message.text == "Да":
        msg = bot.send_message(message.chat.id, "Введите новое время в формате ЧЧ:ММ (24-часовой формат).")
        bot.register_next_step_handler(msg, process_subscription_time)
    elif message.text == "Нет":
        bot.send_message(message.chat.id, "Хорошо, ваше время уведомлений остаётся без изменений.")
        handle_books(message)
    else:
        msg = bot.send_message(message.chat.id, "Пожалуйста, ответьте 'Да' или 'Нет'.")
        bot.register_next_step_handler(msg, process_time_change_decision)


def process_subscription_time(message):
    user_id = message.from_user.id
    try:
        if not re.match(r'^\d{2}:\d{2}$', message.text):
            raise ValueError("Формат времени должен быть ЧЧ:ММ.")

        reminder_time = datetime.strptime(message.text, "%H:%M").time()
        minutes_since_midnight = reminder_time.hour * 60 + reminder_time.minute

        now = datetime.now()
        minutes_since_midnight_now = now.hour * 60 + now.minute

        if reminder_time.hour > 23 or reminder_time.minute > 59:
            raise ValueError("Указано невозможное время.")

        user_data = {
            'chat_id': user_id,
            'username': message.from_user.username,
            'subscribed_at': datetime.now(),
            'reminder_time': minutes_since_midnight
        }

        if minutes_since_midnight < minutes_since_midnight_now:
            current_date = now.date()
            current_datetime = datetime(current_date.year, current_date.month, current_date.day)

            user_data['last_reminder_date'] = current_datetime
        else:
            user_data['last_reminder_date'] = None

        existing_user = users_collection.find_one({'chat_id': user_id})
        if existing_user:
            users_collection.update_one(
                {'chat_id': user_id},
                {'$set': {
                    'reminder_time': user_data['reminder_time'],
                    'last_reminder_date': user_data['last_reminder_date']
                }}
            )
        else:
            users_collection.insert_one(user_data)

        bot.send_message(user_id, "Вы успешно подписались на уведомления о чтении книг!")
        handle_books(message)
    except ValueError as e:
        msg = bot.send_message(user_id, str(e) + " Пожалуйста, введите время ещё раз в формате ЧЧ:ММ.")
        bot.register_next_step_handler(msg, process_subscription_time)


# ------------------------------------------------------------------------------------------------
@bot.message_handler(func=lambda message: message.text == "Отписаться от рассылки")
def text_unsubscribe(message):
    unsubscribe(message)


@bot.message_handler(commands=['unsubscribe'])
def command_unsubscribe(message):
    unsubscribe(message)


def unsubscribe(message):
    user_id = message.chat.id
    existing_user = users_collection.find_one({'chat_id': user_id})
    if existing_user:
        users_collection.delete_one({'chat_id': user_id})
        bot.send_message(user_id, "Вы успешно отписались от ежедневной рассылки!")
    else:
        bot.send_message(user_id, "Вы не подписаны на рассылку!")


# ------------------------------------------------------------------------------------------------
@bot.message_handler(func=lambda message: message.text == "Назад")
def text_back(message):
    start(message)


@bot.message_handler(commands=['back'])
def command_back(message):
    start(message)


# ------------------------------------------------------------------------------------------------
def send_reminder_to_subscribers():
    now = datetime.now()
    current_minutes_since_midnight = now.hour * 60 + now.minute
    current_date = now.date()
    current_datetime = datetime(current_date.year, current_date.month, current_date.day)

    subscribers = users_collection.find({
        "reminder_time": {"$lte": current_minutes_since_midnight},
        "$or": [
            {"last_reminder_date": {"$ne": current_datetime}},
            {"last_reminder_date": {"$exists": False}}
        ]
    })

    for subscriber in subscribers:
        chat_id = subscriber['chat_id']
        print(chat_id)
        bot.send_message(chat_id, "Не забудьте почитать книгу сегодня!")
        users_collection.update_one({'_id': subscriber['_id']}, {"$set": {"last_reminder_date": current_datetime}})
        send_daily_book(chat_id)


# ------------------------------------------------------------------------------------------------
def update_book_of_the_day():
    current_date = datetime.now().date()
    current_datetime = datetime(current_date.year, current_date.month, current_date.day)
    current_bod = books_collection.find_one({'book_of_the_day': True})

    if current_bod and ('last_update' not in current_bod or current_bod['last_update'] < current_datetime):
        exclude_id = current_bod['_id'] if current_bod else None

        if exclude_id:
            books_collection.update_one({'_id': ObjectId(exclude_id)}, {'$set': {'book_of_the_day': False}})

        query = {'_id': {'$ne': ObjectId(exclude_id)}} if exclude_id else {}
        total_books = books_collection.count_documents(query)
        random_index = random.randint(0, total_books - 1)
        new_book_of_the_day = books_collection.find(query).skip(random_index).limit(1).next()

        books_collection.update_one({'_id': new_book_of_the_day['_id']},
                                    {'$set': {'book_of_the_day': True, 'last_update': current_datetime}})
        print("Book of the day updated.")


# ------------------------------------------------------------------------------------------------
def job():
    print("Updating book of the day...")
    update_book_of_the_day()
    print("Sending reminders to subscribers...")
    send_reminder_to_subscribers()


def run_pending():
    while True:
        print('run_pending')
        job()
        time.sleep(60)



schedule_thread = threading.Thread(target=run_pending)
schedule_thread.start()


bot.polling(none_stop=True)
