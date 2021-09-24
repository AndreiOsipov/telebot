import datetime
def get_utc_now_time():
    return datetime.datetime.utcnow()
def format_datetime(full_datetime):
    '''
    эта функция форматирует любое поступающее полное время
    к любому однозначному дню, месяцу или минте будет приписан 0 слева,
    чтобы значение было легко читаемым (не 22.9, а 22.09, не 3:2, а 3:02)
    '''
    day = str(full_datetime.day)
    month = str(full_datetime.month)
    hour = str(full_datetime.hour)
    minute  = str(full_datetime.minute)
    if len(day) == 1:
        day = '0'+day
    if len(month) == 1:
        month = '0'+month
    if len(minute) == 1:
        minute='0'+minute
    formated_date = f'{day}.{month}'
    formated_time = f'{hour}:{minute}'
    return formated_date, formated_time

def remebere_datetime(message_text):
    #получает дату и время из переданновго текста(год 2021 -- не важен, так как функции, получающие отсюда full_datetime
    # используют только месяц, день, час и минуту, год не используется)
    #возваращает текущее дату и время.
    text_list =message_text.split()
    date = text_list[-3]
    time = text_list[-1]
    split_date = date.split('.')
    split_time = time.split(':')
    full_datetime = datetime.datetime.strptime(f'2021-{split_date[1]}-{split_date[0]}-{split_time[0]}-{split_time[1]}', '%Y-%m-%d-%H-%M')
    return full_datetime

def new_time(mode, message_text, time_dif):
    #эта функция выставляет таймер на инлайновом сообщении
    #если таймер на сообщении есть, то в зависимости от нажатой кнопки, будет изменяться выставленное в сообщении время
    #часовой пояс учитывается при создании нового таймера, когда message_text==None, и при сравнении
    #выставленного пользователем времени с текущем.
    #next_datetime берётся из сообщения, при создании которого был учтён часовой пояс(если нет,например старое сообщение 
    # из другого часового пояса, то, если выставленное врмея меньше настоящего, оно будет переведено на настоящие + 1 минута) 
    if time_dif == None:
        time_dif = 0
    if message_text == None:
        next_show_datetime = datetime.datetime.utcnow() + datetime.timedelta(hours=time_dif) + datetime.timedelta(hours=1)
        next_utc_datetime = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        alarm_body = None
    else:
        alarm_body = message_text[message_text.index('<<') : message_text.index('>>')+2]
        message_show_datetime = remebere_datetime(message_text)
        if mode == 'plus_hour':
            next_show_datetime = message_show_datetime + datetime.timedelta(hours=1)
        elif mode == 'plus_minute':
            next_show_datetime = message_show_datetime + datetime.timedelta(minutes=5)
        elif mode == 'plus_one':
            next_show_datetime = message_show_datetime + datetime.timedelta(minutes=1)
        elif mode == 'minus_hour':
            next_show_datetime = message_show_datetime - datetime.timedelta(hours=1)
        elif mode == 'minus_minute':
            next_show_datetime = message_show_datetime - datetime.timedelta(minutes=5)
        elif mode == 'minus_one':
            next_show_datetime = message_show_datetime - datetime.timedelta(minutes=1)

        next_utc_datetime = next_show_datetime - datetime.timedelta(hours=time_dif)
        if next_utc_datetime < datetime.datetime.utcnow():
            next_utc_datetime = datetime.datetime.utcnow() + datetime.timedelta(minutes=1)
            next_show_datetime = datetime.datetime.utcnow() + datetime.timedelta(hours=time_dif) + datetime.timedelta(minutes=1)

    formated_utc_datetime = format_datetime(next_utc_datetime)
    formated_show_datetime = format_datetime(next_show_datetime)
    utc_date = formated_utc_datetime[0]
    utc_time = formated_utc_datetime[1]
    show_date = formated_show_datetime[0]
    show_time = formated_show_datetime[1]
    return utc_date, utc_time, alarm_body, show_date, show_time
