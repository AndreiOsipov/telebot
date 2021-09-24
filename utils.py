import talk_to_bd
import markup_generates
import time
import time_utils
#==================================================================
def general_text_func(from_handler, mode, message):
    '''
    эта функция обрабатывает запросы на создание и изменение таймеров
    если пользоваетль просто напишет что-то боту, будет выставлен новый таймер from_handler == 'text'(message_text == None при поучении full_datetime),
    в случае, если пользователь изменит время на инлайн-клавиатуре, full_datetime будет получен с использованием текста сообщения
    full_datetime -- кортеж из отфарматированных дат и времент для показа и для записи в базу данных.
    всего 5 элементов первые 2 -- дата и время активации по utc для записи в базу, третий -- тело сообщения(то что нужно напомнить)
    последние 2 -- день и время активации таймера по местному времени
    time_dif -- разница между часовым поясом и utc.
    ----Также----
    из-за того, что задача ставится под id сообщения от пользователя,
    а не под id инлайн-ответа бота, все изменения и поиски после обновления таймера с id -1.(id инлайн-ответа на 1 больше)
    '''

    chat_id = message.chat.id
    message_id = message.id
    if from_handler == 'text':
        time_dif = talk_to_bd.find_time_dif(chat_id)
        full_datetime = time_utils.new_time('plus_hour', None, time_dif)
    else:
        time_dif = talk_to_bd.find_time_dif(chat_id)
        full_datetime =  time_utils.new_time(mode, message.text, time_dif)

    utc_date = full_datetime[0]
    utc_time = full_datetime[1]
    alarm_body = full_datetime[2]
    show_date = full_datetime[3]
    show_time = full_datetime[4]

    if alarm_body == None:
        alarm_body = f'<<{message.text}>>'

    resp_text =  f'напомню  {alarm_body}\n{show_date} в {show_time}'#возвращается как текст сообщения
    string_datetime = f'{utc_date} {utc_time}'#отправляется в базу данных
    
    if from_handler == 'text':
        resp_markup = markup_generates.generate_time_markup()
        talk_to_bd.create_new_row(chat_id, alarm_body, string_datetime, message_id)
        return resp_text, resp_markup
    else:
        talk_to_bd.update_timer(chat_id, message_id-1, string_datetime)
        return resp_text
def update_timezone(chat_id, timezone):
    talk_to_bd.commit_timezone(chat_id, timezone)
def confirmation(chat_id, message_id):
    #эта функция только сохраняет поддтверждение(в talk_to_bd.confirmation_misson() оно выстовляется на 1 = подтверждено)
    talk_to_bd.confirmation_misson(chat_id, message_id-1)

def delete_timer(chat_id, message_id):
    talk_to_bd.delete_mission(chat_id, message_id-1)
#================command_resp() и reminder_function(bot) никак не влияют на поступающую информацию ======================================================================================================
#command_resp() -- просто отвечает на команду /start и при необходимости создаёт базу данных
#reminder_function(bot) -- вообзе идёт во втором потоке, она просматривает базу данных каждые 30 секунд
#отправляет "прозвеневшие" напоминанияи сдвигает время у неактивных напоминаний, если оно просрочено
def start_resp():
    talk_to_bd.create_table()
    resp_text = 'Я буду напоминать тебе о делах))Если хочешь включить напоминание, то отправь мне то, о чём нужно напомнить))\nЯ не исполюзую шифрование при хранении информации в базе данных, так что, пожалуйста, не отпраляй сюда пароли/номера карт/номера телефонов и т.д.\nчтобы выставить часовой пояс введи /set_timezone'
    return resp_text

def reminder_function(bot):
    while True:
        time.sleep(10)
        now = time_utils.get_utc_now_time()
        formated_datetime = time_utils.format_datetime(now)
        full_date = formated_datetime[0]
        full_time = formated_datetime[1]
        ids_and_body = talk_to_bd.find_now_alarm(f'{full_date} {full_time}')
        if ids_and_body:
            for i in range(len(ids_and_body)):
               bot.send_message(ids_and_body[i][0], f'напоминаю: {ids_and_body[i][1]}')
               #тут удаляются два сообщения(отправленное пользователем и ответ бота на него)
               bot.delete_message(ids_and_body[i][0], ids_and_body[i][2])
               bot.delete_message(ids_and_body[i][0], ids_and_body[i][2]+1)