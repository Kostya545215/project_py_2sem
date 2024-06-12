import telebot as tb
from telebot import types
bot = tb.TeleBot('6406717020:AAEJYdw0pjQE-cykfr5tzrw3sDmUic8PdQw')

ph = ['Механика', 'Термодинамика и МКТ','Электричество и магнетизм', 'Кинематика', 'Статика', 'Динамика']
    
@bot.message_handler(commands = ['add_problem'])
def add_section(message):
    bot.delete_message(message.chat.id, message.message_id)
    markup = types.InlineKeyboardMarkup(row_width = 1)
    mechanics = types.InlineKeyboardButton('Механика', callback_data = 'add_sub1')
    thermodynamics = tb.types.InlineKeyboardButton('Термодинамика и МКТ', callback_data = 'add_sub2')
    electricity = tb.types.InlineKeyboardButton('Электричество и магнетизм', callback_data = 'add_sub3')
    markup.add(mechanics, thermodynamics, electricity)
    bot.send_message(message.chat.id, '<b>Выберите в какой раздел добавить задачу</b>', reply_markup = markup, parse_mode = 'html')
           
@bot.callback_query_handler(func = lambda callback: callback.data.startswith('add_sub') or callback.data.startswith('level') or callback.data.startswith('text'))    
def add_subsection(callback):
    global section
    if callback.data.startswith('add_sub'):
        markup = types.InlineKeyboardMarkup(row_width = 3)
        m1 = types.InlineKeyboardButton('Кинематика', callback_data = 'level1')
        m2 = types.InlineKeyboardButton('Статика', callback_data = 'level2')
        m3 = types.InlineKeyboardButton('Динамика', callback_data = 'level3')
        markup.add(m1,m2,m3)
        bot.send_message(callback.message.chat.id, 'Выберите подраздел', reply_markup = markup)
        section = ph[int(callback.data[7:]) - 1]
        print(section)
        
    if callback.data.startswith('level'):
        markup = types.InlineKeyboardMarkup(row_width = 2)
        m1 = types.InlineKeyboardButton('1', callback_data = 'text1')
        m2 = types.InlineKeyboardButton('2', callback_data = 'text2')
        m3 = types.InlineKeyboardButton('3', callback_data = 'text3')
        m4 = types.InlineKeyboardButton('4', callback_data = 'text4')
        markup.add(m1,m2,m3,m4)
        bot.send_message(callback.message.chat.id, 'Выберите уровень', reply_markup = markup)
        subsection = ph[int(callback.data[5:]) - 1 + 3]
        print(subsection)
        
    if callback.data.startswith('text'):
        level = int(callback.data[4:])
        print(level)
        texts = bot.send_message(callback.message.chat.id, "Введите текст задачи")
        bot.register_next_step_handler(texts, photo)
        
def photo(message):
    text = message.text
    print(text)
    photo = bot.send_message(message.chat.id, "Введите фотку, если она прилагается к задаче")
    
        
bot.polling(none_stop = True)