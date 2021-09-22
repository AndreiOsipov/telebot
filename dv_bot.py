import utils
from config import TOKEN
import telebot
import markup_generates
import threading

bot = telebot.TeleBot(token=TOKEN)
@bot.callback_query_handler(func=lambda call: True)
def inline_menu(call):
    #какой-то волшебный метод, убирающий кружочек загрузки с инлайн-кнопки
    bot.answer_callback_query(call.id)
    this_message_id = call.message.id
    this_chat_id=call.message.chat.id
    if call.data != 'save' and call.data != 'delete':
        new_text=utils.general_text_func('inline', call.data, call.message)
        bot.edit_message_text(chat_id=this_chat_id,message_id=this_message_id, text=new_text, reply_markup=markup_generates.generate_time_markup())
    elif call.data == 'delete':
        utils.delete_timer(this_chat_id, this_message_id)
        bot.delete_message(this_chat_id, this_message_id)
        
@bot.message_handler(commands=['start'])
def resp_for_command(message):
    text = utils.command_resp()
    bot.send_message(message.chat.id, text)

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