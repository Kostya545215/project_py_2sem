import telebot as tb
from telebot import types
import sqlite3
bot = tb.TeleBot('6406717020:AAEJYdw0pjQE-cykfr5tzrw3sDmUic8PdQw')


# показ главного меню с разделами
def generate_physics_menu(chat_id):
    markup = types.InlineKeyboardMarkup(row_width=1)
    mechanics = types.InlineKeyboardButton('Механика', callback_data='sect1')
    thermodynamics = tb.types.InlineKeyboardButton('Термодинамика и МКТ', callback_data='sect2')
    electricity = tb.types.InlineKeyboardButton('Электричество и магнетизм', callback_data='sect3')
    optics = tb.types.InlineKeyboardButton('Оптика', callback_data='sect4')
    quantums = tb.types.InlineKeyboardButton('Квантовая и ядерная физика', callback_data='sect5')
    markup.add(mechanics, thermodynamics, electricity, optics, quantums)
    bot.send_message(chat_id, '<b>Выберите раздел физики</b>', reply_markup=markup, parse_mode='html') 


# Функция которая запускает бота и выводит меню разделов при написании команды /start
@bot.message_handler(commands=['start'])
def topic(message):
    bot.delete_message(message.chat.id, message.message_id)
    generate_physics_menu(message.chat.id)


# Переход к разделам
@bot.message_handler(func=lambda message: message.text.lower() == 'к разделам')
def handle_sections_text(message):
    generate_physics_menu(message.chat.id)


# Переход к подразделам
@bot.callback_query_handler(func=lambda callback: callback.data == 'sections')
def topic(callback):
    bot.delete_message(callback.message.chat.id, callback.message.message_id)
    generate_physics_menu(callback.message.chat.id)


# Вывод ответа
@bot.callback_query_handler(func=lambda callback: callback.data.startswith('ans_'))
def ans(callback):
    # bot.delete_message(callback.message.chat.id, callback.message.message_id)
    bot.send_message(callback.message.chat.id, f'{callback.data[4:]}')


num = [0]
max_task = [0]


# блок функций действующих после нажатий кнопок
@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    # реализация меню подразделов
    def subsection(section, *args):
        c = 0
        buttons = []
        for i in args:
            c += 1 
            buttons.append(types.InlineKeyboardButton(str(i), callback_data=f'{section}_{c}'))
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(*buttons)
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        bot.send_message(callback.message.chat.id, f'<b>Выберите подраздел</b>', reply_markup=markup, parse_mode='html')

    sections = {
        'sect1': ('sect1', 'Кинематика', 'Динамика', 'Статика'),
        'sect2': ('sect2', 'Молекулярная физика', 'Изопроцессы', 'Влажность', 'Тепловые процессы'),
        'sect3': ('sect3', 'Электростатика', 'Электродинамика', 'Электромагнитные волны', 'Магнетизм'),
        'sect4': ('sect4', 'Геометрическая оптика', 'Волновая оптика'),
        'sect5': ('sect5', 'Квантовая механика', 'Радиоактивность', 'Специальная теория относительности'),
    }

    if callback.data in sections:
        subsection(*sections[callback.data])
    # реализация выбора сложности задачи
    if callback.data.startswith('sect') and len(list(map(str, callback.data.split('_')))) == 2:
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        markup = types.InlineKeyboardMarkup(row_width=2)
        first = types.InlineKeyboardButton('1', callback_data=f'{callback.data}_1')
        second = types.InlineKeyboardButton('2', callback_data=f'{callback.data}_2')
        third = types.InlineKeyboardButton('3', callback_data=f'{callback.data}_3')
        fourth = types.InlineKeyboardButton('4', callback_data=f'{callback.data}_4')
        markup.add(first, second, third, fourth)

        bot.send_message(callback.message.chat.id, 'Выберите уровень сложности', reply_markup=markup)
    # Показ задачи, ее картинки, и перелистывание задач
    if (callback.data.startswith('sect') and len(list(map(str, callback.data.split('_')))) == 3
            or callback.data[-4:] == 'back' or callback.data[-4:] == 'next'):
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        callback_subsection = str(callback.data)[:5]
        print(callback.data)

        search = callback.data.split('_')
        section = search[0]
        subsection = search[1]
        diff = search[2]
        
        if callback.data[-4:] in ('next', 'back'):
            if callback.data[-4:] == 'next':
                num[0] = (num[0] + 1) % max_task[0]
            else:  # callback.data[-4:] == 'back'
                num[0] = (num[0] - 1) % max_task[0]
            callback.data = callback.data[:9]
        callback.data = callback.data[:9]
        # вывод задачи из БД
        conn = sqlite3.connect('физика.db')
        cursor = conn.cursor()
        cursor.execute(
            'SELECT задача, ответ, фото  FROM задачи \
             WHERE раздел=? AND подраздел = ? AND сложность = ? ORDER BY сложность LIMIT ?,1 ',
            (section, subsection, diff, num[0]))
        t = cursor.fetchone()
        task = t[0]
        ans = t[1]

        cursor.execute(
            'SELECT count(задача)  FROM задачи  WHERE раздел=? AND подраздел = ? AND сложность = ? ORDER BY сложность ',
            (section, subsection, diff))
        max_task[0] = int(cursor.fetchone()[0])
        # реализация кнопок переходов к задачам, разделам, подразделам и вывода ответа
        markup = types.InlineKeyboardMarkup(row_width=3)
        last_task = types.InlineKeyboardButton('Прошлая задача', callback_data=f'{callback.data}_back')
        next_task = types.InlineKeyboardButton('Cледующая задача', callback_data=f'{callback.data}_next')
        answer = types.InlineKeyboardButton('Ответ', callback_data=f'ans_{ans}')
        sections = types.InlineKeyboardButton('К разделам', callback_data='sections')
        subsections = types.InlineKeyboardButton('К подразделам', callback_data=callback_subsection)
        markup.add(last_task, answer, next_task, sections, subsections)
        # вывод картинки к задаче при ее наличии
        try:
            img = str(t[2])
            photo = open(img, 'rb')
            bot.send_photo(callback.message.chat.id, photo, caption=f'{task} ', reply_markup=markup)
        except Exception:
            bot.send_message(callback.message.chat.id, f'{task} ', reply_markup=markup)


bot.polling(none_stop=True)
