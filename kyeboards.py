from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import admins

# old = open('menu.png', 'rb')
inline_btn_1 = InlineKeyboardButton('Зареєструватися в черзі', callback_data='register')
inline_btn_2 = InlineKeyboardButton('Взнати номер в черзі', callback_data='what are your number')
inline_btn_3 = InlineKeyboardButton('Наступний номер до реєстратора', callback_data='last number')
inline_btn_4 = InlineKeyboardButton('Локація де реєструют', callback_data='location_office')
inline_btn_5 = InlineKeyboardButton('Довідка', callback_data='info')
inline_btn_6 = InlineKeyboardButton('Про заклад', url='https://www.facebook.com/right2protection/')
inline_btn_admin = InlineKeyboardButton('ADMIN', callback_data='admin_menu')
inline_btn_back = InlineKeyboardButton('BACK', callback_data='start')
inline_btn_cancel = InlineKeyboardButton('CANCEL', callback_data='cancelll')
inline_btn_pass_new = InlineKeyboardButton(f'1️⃣ ID CARD', callback_data='new_pas')
inline_btn_pass_old = InlineKeyboardButton('2️⃣ PASSPORT', callback_data='old_pas')
link = 'https://docs.google.com/spreadsheets/d/10k_JBibHN8CyXYmMjD27VtnaVf-M11aeFKQv1ahKG50/edit#gid=69334046'
inline_btn_link = InlineKeyboardButton('Exel', url=link)
inline_btn_ch_status = InlineKeyboardButton('Change Status', callback_data='change_status')
inline_btn_message = InlineKeyboardButton('Відправити повідомлення', callback_data='send_message')

inline_kb_start_user = InlineKeyboardMarkup().\
    add(inline_btn_1).\
    add(inline_btn_2).\
    add(inline_btn_3).\
    add(inline_btn_4).\
    add(inline_btn_5, inline_btn_6)
inline_kb_start_user_admin = InlineKeyboardMarkup().\
    add(inline_btn_1).\
    add(inline_btn_2).\
    add(inline_btn_3).\
    add(inline_btn_4).\
    add(inline_btn_5, inline_btn_6).\
    add(inline_btn_admin)
inline_kb_admin = InlineKeyboardMarkup().add(inline_btn_admin, inline_btn_back)
inline_kb_admin_2 = InlineKeyboardMarkup().add(inline_btn_ch_status, inline_btn_back)
inline_kb_admin_3 = InlineKeyboardMarkup().add(inline_btn_ch_status, inline_btn_back).add(inline_btn_message)
inline_back = InlineKeyboardMarkup().add(inline_btn_back)
inline_cancel = InlineKeyboardMarkup().add(inline_btn_back, inline_btn_cancel)
inline_kb_cancel = InlineKeyboardMarkup().add(inline_btn_cancel)
inline_kb_choose_pass = InlineKeyboardMarkup().add(inline_btn_pass_new, inline_btn_pass_old)
inline_kb_admin_menu = InlineKeyboardMarkup().add(inline_btn_link).add(inline_btn_ch_status).add(inline_btn_back)


def kb_user(user):
    if str(user) in admins:
        kb = inline_kb_start_user_admin
    else:
        kb = inline_kb_start_user
    return kb
