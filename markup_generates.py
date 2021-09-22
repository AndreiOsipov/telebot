from telebot import types
def generate_time_markup():
    #-----------кнопочки-----------
    add_hour_button = types.InlineKeyboardButton('+ час', callback_data='plus_hour')
    add_minute_button = types.InlineKeyboardButton('+ 5 минут', callback_data='plus_minute')
    minus_hour_button = types.InlineKeyboardButton('- час', callback_data='minus_hour')
    minus_minute_button = types.InlineKeyboardButton('- 5 минут', callback_data='minus_minute')
    pluse_one_button = types.InlineKeyboardButton('+ 1 минута', callback_data='pluse_one')
    minuse_one_button = types.InlineKeyboardButton('- 1 минута', callback_data='minus_one')
    delete_timer_button = types.InlineKeyboardButton('удалить этот таймер', callback_data='delete')
    #-----------клава-----------
    time_menu_inline = types.InlineKeyboardMarkup(row_width=3)
    time_menu_inline.add(add_hour_button, add_minute_button, pluse_one_button, minus_hour_button, minus_minute_button, minuse_one_button) 
    time_menu_inline.add(delete_timer_button)
    return time_menu_inline

