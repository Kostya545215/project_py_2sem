import telebot as tb
from telebot import types
import sqlite3
bot = tb.TeleBot('6406717020:AAEJYdw0pjQE-cykfr5tzrw3sDmUic8PdQw')
    
@bot.message_handler(commands = ['add_problem'])
def add_section(message):
    bot.delete_message(message.chat.id, message.message_id)
    markup = types.InlineKeyboardMarkup(row_width = 1)
    mechanics = types.InlineKeyboardButton('Механика', callback_data = 'add_sub')
    thermodynamics = tb.types.InlineKeyboardButton('Термодинамика и МКТ', callback_data = 'add_sub')
    electricity = tb.types.InlineKeyboardButton('Электричество и магнетизм', callback_data = 'add_sub')
    optics = tb.types.InlineKeyboardButton('Оптика', callback_data = 'add_sub')
    quantums = tb.types.InlineKeyboardButton('Квантовая и ядерная физика', callback_data = 'add_sub')
    markup.add(mechanics, thermodynamics, electricity, optics, quantums)
    bot.send_message(message.chat.id, '<b>Выберите в какой раздел добавить задачу</b>', reply_markup = markup, parse_mode = 'html')
    
@bot.message_handler(commands = ['start'])
def topic(message):
    
    conn = sqlite3.connect('physics.sql')
    cur = conn.cursor()
    cur.execute( 'CREATE TABLE IF NOT EXISTS problems ( id INT AUTO_INCREMENT, section VARCHAR(30), subsection VARCHAR(30), content TEXT, pic IMAGE)' )
    conn.commit()
    cur.close()
    conn.close()    

    bot.delete_message(message.chat.id, message.message_id)
    markup = types.InlineKeyboardMarkup(row_width = 1)
    mechanics = types.InlineKeyboardButton('Механика', callback_data = 'mechs')
    thermodynamics = tb.types.InlineKeyboardButton('Термодинамика и МКТ', callback_data = 'mechs')
    electricity = tb.types.InlineKeyboardButton('Электричество и магнетизм', callback_data = 'mechs')
    optics = tb.types.InlineKeyboardButton('Оптика', callback_data = 'mechs')
    quantums = tb.types.InlineKeyboardButton('Квантовая и ядерная физика', callback_data = 'mechs')
    markup.add(mechanics, thermodynamics, electricity, optics, quantums)
    bot.send_message(message.chat.id, '<b>Выберите раздел физики</b>', reply_markup = markup, parse_mode = 'html')    
    
    
@bot.callback_query_handler(func = lambda callback: callback.data.startswith('add_sub') or callback.data == 'level' or callback.data == 'text')    
def add_subsection(callback):
    if callback.data == 'add_sub':
        markup = types.InlineKeyboardMarkup(row_width = 3)
        m1 = types.InlineKeyboardButton('Кинематика', callback_data = 'level')
        m2 = types.InlineKeyboardButton('Статика', callback_data = 'level')
        m3 = types.InlineKeyboardButton('Динамика', callback_data = 'level')
        markup.add(m1,m2,m3)
        bot.send_message(callback.message.chat.id, 'Выберите подраздел', reply_markup = markup)
        
    if callback.data == 'level':
        markup = types.InlineKeyboardMarkup(row_width = 2)
        m1 = types.InlineKeyboardButton('1', callback_data = 'text')
        m2 = types.InlineKeyboardButton('2', callback_data = 'text')
        m3 = types.InlineKeyboardButton('3', callback_data = 'text')
        m4 = types.InlineKeyboardButton('4', callback_data = 'text')
        markup.add(m1,m2,m3,m4)
        bot.send_message(callback.message.chat.id, 'Выберите уровень', reply_markup = markup)       
        
    if callback.data == 'text':
        mess = bot.send_message(callback.message.chat.id, "Введите текст задачи")
        bot.register_next_step_handler(mess, photo)
            
def photo(message):
    bot.send_message(message.chat.id, "Введите фотку, если она прилагается к задаче")
    
    
@bot.callback_query_handler(func = lambda callback: callback.data.startswith('mechs'))
def callback_message(callback):
    if callback.data == 'mechs':
        markup = types.InlineKeyboardMarkup(row_width = 3)
        kin = types.InlineKeyboardButton('Кинематика', callback_data = 'mechs1')
        din = tb.types.InlineKeyboardButton('Динамика', callback_data = 'mechs2')
        stat = tb.types.InlineKeyboardButton('Статика', callback_data = 'mechs3')
        markup.add(kin,din,stat)
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        bot.send_message(callback.message.chat.id, '<b>Выберите подраздел механики</b>', reply_markup = markup, parse_mode = 'html')
          
    if callback.data == 'mechs1':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        bot.send_message(callback.message.chat.id, 'Спасибо, что выбрали этот раздел')
    if callback.data == 'mechs2':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        bot.send_message(callback.message.chat.id, 'Спасибо, что выбрали именно этот раздел')
    if callback.data == 'mechs3':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        bot.send_message(callback.message.chat.id, 'Спасибо, что выбрали эээээ раздел')    
        
bot.polling(none_stop = True)