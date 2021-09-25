import utils
from config import TOKEN
import telebot
import markup_generates
import threading
import talk_to_bd

talk_to_bd.create_table()
bot = telebot.TeleBot(token=TOKEN)
@bot.callback_query_handler(func=lambda call: True)
def inline_menu(call):
    #какой-то волшебный метод, убирающий кружочек загрузки с инлайн-кнопки
    bot.answer_callback_query(call.id)
    this_message_id = call.message.id
    this_chat_id=call.message.chat.id

    timer_call_list = [
        'plus_hour', 'plus_minute', 'plus_one',
        'minus_hour', 'minus_minute', 'minus_one',
    ]

    if call.data in timer_call_list:
        new_text=utils.general_text_func('inline', call.data, call.message)
        bot.edit_message_text(chat_id=this_chat_id,message_id=this_message_id, text=new_text, reply_markup=markup_generates.generate_time_markup())
    elif call.data == 'delete':
        utils.delete_timer(this_chat_id, this_message_id)
        bot.delete_message(this_chat_id, this_message_id)
    elif call.data == 'update_tz':
        try:
            bot.edit_message_text(chat_id=this_chat_id, message_id=this_message_id, text='выбери из этих часовых поясов', reply_markup=markup_generates.generate_timezone_markup())
        except:
            pass
    else:
        utils.update_timezone(this_chat_id, int(call.data))
        try:
            bot.edit_message_text(chat_id=this_chat_id, message_id=this_message_id, text='можешь в любой момент изменить выбор: ', reply_markup=markup_generates.generate_timezone_markup())
            bot.send_message(chat_id=this_chat_id, text='часвой пояс выбран')
        except:
            pass
@bot.message_handler(commands=['start'])
def resp_for_start(message):
    text = utils.start_resp()
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['set_timezone'])
def retirn_set_timezone(message):
    text = 'выбери часовой пояс из прдложенных(сможешь сменить его в любой момент, введя эту команду/set_timezone)'
    bot.send_message(message.chat.id, text, reply_markup=markup_generates.generate_timezone_markup())
    
@bot.message_handler(content_types=['text'])
def resp_for_text(message):
    resp = utils.general_text_func('text', 'plus_hour', message)
    text = resp[0]
    markup = resp[1]
    bot.send_message(message.chat.id, text, reply_markup=markup)

if __name__ == '__main__':
    get = threading.Thread(target=bot.infinity_polling)
    post = threading.Thread(target=utils.reminder_function, args=(bot, ))
    get.start()
    post.start()
