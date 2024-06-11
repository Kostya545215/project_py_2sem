import telebot as tb
from telebot import types
bot = tb.TeleBot('6406717020:AAEJYdw0pjQE-cykfr5tzrw3sDmUic8PdQw')


def generate_physics_menu(chat_id):
    markup = types.InlineKeyboardMarkup(row_width=1)
    mechanics = types.InlineKeyboardButton('Механика', callback_data='sect1')
    thermodynamics = tb.types.InlineKeyboardButton('Термодинамика и МКТ', callback_data='sect2')
    electricity = tb.types.InlineKeyboardButton('Электричество и магнетизм', callback_data='sect3')
    optics = tb.types.InlineKeyboardButton('Оптика', callback_data='sect4')
    quantums = tb.types.InlineKeyboardButton('Квантовая и ядерная физика', callback_data='sect5')
    markup.add(mechanics, thermodynamics, electricity, optics, quantums)
    bot.send_message(chat_id, '<b>Выберите раздел физики</b>', reply_markup=markup, parse_mode='html') 

@bot.message_handler(commands = ['start'] )
def topic(message):
    bot.delete_message(message.chat.id, message.message_id)
    generate_physics_menu(message.chat.id)

@bot.message_handler(func=lambda message: message.text.lower() == 'к разделам')
def handle_sections_text(message):
    generate_physics_menu(message.chat.id)

@bot.callback_query_handler(func = lambda callback : callback.data == 'sections')
def topic(callback):
    bot.delete_message(callback.message.chat.id, callback.message.message_id)
    generate_physics_menu(callback.message.chat.id)

@bot.callback_query_handler(func = lambda callback : callback.data == 'ans')
def topic(callback):
    bot.delete_message(callback.message.chat.id, callback.message.message_id)
    pass

@bot.callback_query_handler(func = lambda callback: True)
def callback_message(callback):
    def subsection(section, *args):
        c = 0
        buttons = []
        for i in args:
            c += 1 
            buttons.append(types.InlineKeyboardButton(str(i), callback_data = f'{section}_{c}'))
        markup = types.InlineKeyboardMarkup(row_width = 2)
        markup.add(*buttons)
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        bot.send_message(callback.message.chat.id, f'<b>Выберите подраздел</b>', reply_markup = markup, parse_mode = 'html')

    if callback.data == 'sect1':
        subsection('sect1', 'Кинематика', 'Динамика', 'Статика')
    if callback.data == 'sect2':
        subsection('sect2', 'Молекулярная физика', 'Изопроцессы', 'Влажность', 'Тепловые процессы')
    if callback.data == 'sect3':
        subsection('sect3', 'Электростатика', 'Электродинамика', 'Электромагнитные волны', 'Магнетизм')
    if callback.data == 'sect4':
        subsection('sect4', 'Геометрическая оптика', 'Волновая оптика')
    if callback.data == 'sect5':
        subsection('sect5', 'Квантовая механика', 'Радиоактивность', 'Специальная теория относительности')
        
    if callback.data.startswith('sect') and len(list(map(str, callback.data.split('_')))) == 2:
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        print(callback.data)
        markup = types.InlineKeyboardMarkup(row_width = 2)
        first = types.InlineKeyboardButton('1', callback_data = f'{callback.data}_1')
        second = types.InlineKeyboardButton('2', callback_data = f'{callback.data}_2')
        third = types.InlineKeyboardButton('3', callback_data = f'{callback.data}_3')
        fourth = types.InlineKeyboardButton('4', callback_data = f'{callback.data}_4')
        markup.add(first, second, third, fourth)

        bot.send_message(callback.message.chat.id, 'Выберите уровень сложности', reply_markup = markup )

    if callback.data.startswith('sect') and len(list(map(str, callback.data.split('_')))) == 3:
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        callback_subsection = str(callback.data)[:-4]
        print(callback.data)
        markup = types.InlineKeyboardMarkup(row_width = 3)
        last_task = types.InlineKeyboardButton('Прошлая задача', callback_data = 'back')
        next_task = types.InlineKeyboardButton('Cледующая задача', callback_data = 'next')
        answer = types.InlineKeyboardButton('Ответ', callback_data = 'ans')
        sections = types.InlineKeyboardButton('К разделам', callback_data = 'sections')
        subsections = types.InlineKeyboardButton('К подразделам', callback_data = callback_subsection)
        markup.add(last_task, answer, next_task, sections, subsections)
        photo = open('cats_geometry.jpg', 'rb')
        bot.send_photo(callback.message.chat.id, photo, caption = f'Здесь выводится текст задачи, идет подключение к БД. \
Выбор задачи должен быть по ключу - {callback.data} (ключ разный у каждой кнопки подраздела)', reply_markup = markup)


bot.polling(none_stop = True)

