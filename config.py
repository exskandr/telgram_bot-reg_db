import os
from dotenv import load_dotenv


load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
admin_id = os.getenv('ADMIN_ID')
admins = os.getenv('ADMINS')
admins = eval(admins)
channel_id = os.getenv('CHANNEL_ID')


# # Координати
# вулиця Героїв Майдану, 28/78, Хмельницький, Хмельницька область, 29000
# lat = 49.42191605679186
# lon = 26.982433044244683

address = "м. Хмельницький, вул. Михайла Грушевського, 52 (3 поверх, к.32)"
lat = 49.42545091070212
lon = 26.986254848687384
# 49.425417, 26.986231
