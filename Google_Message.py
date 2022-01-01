from Google_Module import Create_Service
import base64
from apscheduler.schedulers.blocking import BlockingScheduler
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from datetime import timedelta
import time


CLIENT_SECRET_FILE = 'client_secret_2.json'
API_NAME = 'gmail'
API_VERSION = 'v1'
SCOPES = ['https://mail.google.com/']

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

while True:
    fecha_str = input('Ingrese fecha y hora de inicio del experimento con el siguiente formato (dd/mm/aaaa-hh:mm): ')
    Duracionexp = int(input("Ingrese la duración del experimento (en minutos): "))
    try:
        fecha = datetime.strptime(fecha_str, '%d/%m/%Y-%H:%M')
        fecha_1= type(fecha)

    except ValueError:
        print("No ha ingresado una fecha correcta")
    else:
        break
#--------------------------------------------------------------------------------------------------
def my_job1(message1):
#def test():

#---------------------------------------------------------------------------------------------------
   #Mensaje que se envía

    emailMsg_1 = '''<!DOCTYPE html>
<html>
    <body>
        <h1 style="color:SlateGray;">1er Mensaje de experimento</h1>
    </body>
</html>
'''

#--------------------------------------------------------------------------------------------------------
   #Envío del primer correo
   
    mimeMessage1 = MIMEMultipart()
    mimeMessage1['to'] = 'sg.mejiar@alum.up.edu.pe' # Destinatarios (Cuentas de correos)
    mimeMessage1['subject'] = 'Mensaje enviado desde Python 1'
    mimeMessage1.attach(MIMEText(emailMsg_1, 'html'))
    raw_string1 = base64.urlsafe_b64encode(mimeMessage1.as_bytes()).decode()

    message1 = service.users().messages().send(userId='me', body={'raw': raw_string1}).execute()
    
    global running
    running = False

    print(message1)
    print("El primer correo ya fue enviado.")


#---------------------------------------------------------------------------------------------------------------
def my_job2(message2):
#def test():

#---------------------------------------------------------------------------------------------------
   #Mensaje que se envía

    emailMsg_2 = '''<!DOCTYPE html>
<html>
    <body>
        <h1 style="color:SlateGray;">2do Mensaje de experimento</h1>
    </body>
</html>
'''

#--------------------------------------------------------------------------------------------------------
   #Envío del segundo correo
   
    mimeMessage2 = MIMEMultipart()
    mimeMessage2['to'] = 'sg.mejiar@alum.up.edu.pe' # Destinatarios (Cuentas de correos)
    mimeMessage2['subject'] = 'Mensaje enviado desde Python 2'
    mimeMessage2.attach(MIMEText(emailMsg_2, 'html'))
    raw_string2 = base64.urlsafe_b64encode(mimeMessage2.as_bytes()).decode()

    message2 = service.users().messages().send(userId='me', body={'raw': raw_string2}).execute()
    
    global running
    running = False

    print(message2)
    print("El segundo correo ya fue enviado.")

#----------------------------------------------------------------------------------------------------------------
def my_job3(message3):
#def test():
#---------------------------------------------------------------------------------------------------
   #Mensaje que se envía

    emailMsg_3 = '''<!DOCTYPE html>
<html>
    <body>
        <h1 style="color:SlateGray;">3er Mensaje de experimento</h1>
    </body>
</html>
'''
#--------------------------------------------------------------------------------------------------------
   #Envío del tercer correo
   
    mimeMessage3 = MIMEMultipart()
    mimeMessage3['to'] = 'sg.mejiar@alum.up.edu.pe' # Destinatarios (Cuentas de correos)
    mimeMessage3['subject'] = 'Mensaje enviado desde Python 3'
    mimeMessage3.attach(MIMEText(emailMsg_3, 'html'))
    raw_string3 = base64.urlsafe_b64encode(mimeMessage3.as_bytes()).decode()

    message3 = service.users().messages().send(userId='me', body={'raw': raw_string3}).execute()
    
    global running
    running = False

    print(message3)
    print("El tercer correo ya fue enviado.")

#---------------------------------------------------------------------------------------------------------------
    #Horas de envío programadas

sched = BlockingScheduler()

now = datetime.now()

delta = fecha - now

if delta > timedelta(0):
    target1 = fecha - timedelta(minutes=30)
    target2= fecha - timedelta(minutes=1)
    target3= fecha + timedelta(minutes= Duracionexp)

    sched.add_job(my_job1, 'date', run_date=((target1)), args=['text'])
    print("El primer correo será enviado (30 minutos antes del inicio): ")
    print(target1)

    sched.add_job(my_job2, 'date', run_date=((target2)), args=['text'])
    print("El segundo correo será enviado (1 minuto antes del inicio): ")
    print(target2)
    
    sched.add_job(my_job3, 'date', run_date=((target3)), args=['text'])
    print("El tercer correo será enviado al finalizar el experimento: ")
    print(target3)

    sched.start()
        
