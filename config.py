from datetime import datetime, date, time
import os

token = os.environ.get('Bot_Toketn')#telegram API
passe = os.environ.get('SQL_pass')#pgSQL API
opWM = os.environ.get('OpenWeatherMap')#OWM API

dt = datetime.today()
day_th = dt.date() # Текущая дата
