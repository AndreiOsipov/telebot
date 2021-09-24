import datetime
from telebot import types
import time_utils
def generate_time_markup():
    #-----------кнопочки-----------
    add_hour_button = types.InlineKeyboardButton('+ час', callback_data='plus_hour')
    add_minute_button = types.InlineKeyboardButton('+ 5 минут', callback_data='plus_minute')
    minus_hour_button = types.InlineKeyboardButton('- час', callback_data='minus_hour')
    minus_minute_button = types.InlineKeyboardButton('- 5 минут', callback_data='minus_minute')
    pluse_one_button = types.InlineKeyboardButton('+ 1 минута', callback_data='plus_one')
    minuse_one_button = types.InlineKeyboardButton('- 1 минута', callback_data='minus_one')
    delete_timer_button = types.InlineKeyboardButton('удалить этот таймер', callback_data='delete')
    #-----------клава-----------
    time_menu_inline = types.InlineKeyboardMarkup(row_width=3)
    time_menu_inline.add(add_hour_button, add_minute_button, pluse_one_button, minus_hour_button, minus_minute_button, minuse_one_button) 
    time_menu_inline.add(delete_timer_button)
    return time_menu_inline

def generate_timezone_markup():
    set_tz_markup = types.InlineKeyboardMarkup(row_width=3)
    for i in range(-11, 12, 3):
        button_list = []
        for j in range(3):
            full_datetime = datetime.datetime.utcnow()
            timezone_datetime = full_datetime + datetime.timedelta(hours=i+j)
            formated_datetime = time_utils.format_datetime(timezone_datetime)
            now_day = formated_datetime[0]
            now_time = formated_datetime[1]
            tz_time = f'{now_day} {now_time}'
            button_list.append(tz_time)
        button1 = types.InlineKeyboardButton(button_list[0], callback_data=f'{str(i)}')
        button2 = types.InlineKeyboardButton(button_list[1], callback_data=f'{str(i+1)}')
        button3 = types.InlineKeyboardButton(button_list[2], callback_data=f'{str(i+2)}')
        
        set_tz_markup.add(button1, button2, button3)
    set_tz_markup.add(types.InlineKeyboardButton('Обновить часовые пояса', callback_data='update_tz'))
    return set_tz_markup
