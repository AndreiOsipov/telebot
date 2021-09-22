import talk_to_bd
import markup_generates
import datetime
import time   
def remebere_datetime(message_text):
    #получает дату и время из переданновго текста(год 2021 -- не важен, так как функции, получающие отсюда full_datetime
    # используют только месяц, день, час и минуту, год не используется)
    text_list =message_text.split()
    date = text_list[-3]
    time = text_list[-1]
    split_date = date.split('.')
    split_time = time.split(':')
    full_datetime = datetime.datetime.strptime(f'2021-{split_date[1]}-{split_date[0]}-{split_time[0]}-{split_time[1]}', '%Y-%m-%d-%H-%M')
    return full_datetime

def new_time(mode, message_text):
    #эта функция выставляет таймер на инлайновом сообщении
    #если таймер на сообщении естьЮ то в зависимости от нажатой кнопки, будет изменяться выставленное в сообщении время
    if message_text == None:

        next_datetime =  datetime.datetime.now() + datetime.timedelta(hours=1)
        alarm_body = None

    else:
        alarm_body = message_text[message_text.index('<<') : message_text.index('>>')+2]

        full_datetime = remebere_datetime(message_text)
        if mode == 'plus_hour':
            next_datetime = full_datetime + datetime.timedelta(hours=1)
        elif mode == 'plus_minute':
            next_datetime = full_datetime + datetime.timedelta(minutes=5)
        elif mode == 'pluse_one':
            next_datetime = full_datetime + datetime.timedelta(minutes=1)
        elif mode == 'minus_hour':
            next_datetime = full_datetime - datetime.timedelta(hours=1)
        elif mode == 'minus_minute':
            next_datetime = full_datetime - datetime.timedelta(minutes=5)
        elif mode == 'minus_one':
            next_datetime = full_datetime - datetime.timedelta(minutes=1)

        if next_datetime < datetime.datetime.now():
            next_datetime = datetime.datetime.now() + datetime.timedelta(minutes=1)

    next_day = next_datetime.day
    next_month = next_datetime.month
    next_hour = next_datetime.hour
    next_minute = next_datetime.minute

    if len(str(next_datetime.day)) == 1:
        next_day = '0'+str(next_datetime.day)
    if len(str(next_datetime.month)):
        next_month = '0'+str(next_datetime.month)
    if len(str(next_datetime.minute)) == 1:
        next_minute = '0'+str(next_datetime.minute)

    next_hour = next_datetime.hour
    alarm_date = f'{next_day}.{next_month}'
    alarm_time = f'{next_hour}:{next_minute}'
    return alarm_date, alarm_time, alarm_body
#==================================================================
'''
new_text() и text_func() - очень похожие функции
каждая из них получает 
'''
def general_text_func(from_handler, mode, message):
    chat_id = message.chat.id
    message_id = message.id

    if from_handler == 'text':
        full_datetime = new_time(mode='plus_hour', message_text=None)
    else:
        full_datetime =  new_time(mode, message.text)

    full_date = full_datetime[0]
    full_time = full_datetime[1]
    alarm_body = full_datetime[2]
    if alarm_body == None:
        alarm_body = f'<<{message.text}>>'

    string_datetime = f'{full_date} {full_time}'#отправляется в базу данных
    resp_text =  f'напомню  {alarm_body}\n{full_date} в {full_time}'#возвращается как текст сообщения

    if from_handler == 'text':
        resp_markup = markup_generates.generate_time_markup()
        talk_to_bd.create_new_row(chat_id, alarm_body, string_datetime, message_id)
        return resp_text, resp_markup
    else:
        talk_to_bd.update_timer(chat_id, message_id-1, string_datetime)
        return resp_text

def confirmation(chat_id, message_id):
    #эта функция только сохраняет поддтверждение(в talk_to_bd.confirmation_misson() оно выстовляется на 1 = подтверждено)
    talk_to_bd.confirmation_misson(chat_id, message_id-1)

def delete_timer(chat_id, message_id):
    talk_to_bd.delete_mission(chat_id, message_id-1)
#================command_resp() и reminder_function(bot) никак не влияют на поступающую информацию ======================================================================================================
#command_resp() -- просто отвечает на команду /start и при необходимости создаёт базу данных
#reminder_function(bot) -- вообзе идёт во втором потоке, она просматривает базу данных каждые 30 секунд
#отправляет "прозвеневшие" напоминанияи сдвигает время у неактивных напоминаний, если оно просрочено
def command_resp():
    talk_to_bd.create_table()
    resp_text = 'Я буду напоминать тебе о делах))Если хочешь включить напоминание, то отправь мне то, о чём нужно напомнить))\nЯ не исполюзую шифрование при хранении информации в базе данных, так что, пожалуйста, не отпраляй сюда пароли/номера карт/номера телефонов и т.д.'
    return resp_text

def reminder_function(bot):
    while True:
        time.sleep(10)
        now = datetime.datetime.now()
        now_day = now.day
        now_month = now.month
        now_hour = now.hour
        now_minute = now.minute

        if len(str(now_day)) == 1:
            now_day = '0'+str(now_day)
        if len(str(now_month)):
            now_month = '0'+str(now_month)
        if len(str(now_minute)) == 1:
            now_minute = '0'+str(now_minute)

        full_date = f'{now_day}.{now_month}'
        full_time = f'{now_hour}:{now_minute}'
        ids_and_body = talk_to_bd.find_now_alarm(f'{full_date} {full_time}')
        if ids_and_body:
            for i in range(len(ids_and_body)):
               bot.send_message(ids_and_body[i][0], f'напоминаю: {ids_and_body[i][1]}')
               #тут удаляются два сообщения(отправленное пользователем и ответ бота на него)
               bot.delete_message(ids_and_body[i][0], ids_and_body[i][2])
               bot.delete_message(ids_and_body[i][0], ids_and_body[i][2]+1)