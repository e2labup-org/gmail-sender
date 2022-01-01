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
sched = BlockingScheduler()
#mensaje que se desea enviar 
def E2lab_Message(email):

    message = '''
                <!DOCTYPE html>
                <html>
                    <body>
                        <h1 style="color:SlateGray;">Hola Mundo! Te escribimos del E2labUP</h1>
                    </body>
                </html>
            '''  

    mimeMessage1 = MIMEMultipart()
    mimeMessage1['to'] = email # Destinatario (Cuentas de correos)
    mimeMessage1['subject'] = 'Mensaje Prueba del E2labUP'
    mimeMessage1.attach(MIMEText(message, 'html'))
    raw_string1 = base64.urlsafe_b64encode(mimeMessage1.as_bytes()).decode()

    message1 = service.users().messages().send(userId='me', body={'raw': raw_string1}).execute()
    
    global running
    running = False

    print(message1)
    print("El correo de prueba acaba de ser enviado")
    
#Formato de la fecha (ingresar como string): dd/mm/aaaa-hh:mm
def E2lab_send_message(email,fecha):

    fecha = datetime.strptime(fecha, '%d/%m/%Y-%H:%M')
    #
    # Codigo que retiene el correo por un determinado tiempo
    # para de ahi mandarlo
    print("Mail para: "+email+" y llegará el: "+str(fecha))
    E2lab_Message(email) #manda el mail
    

#testeando el envio del mensaje: 
E2lab_send_message('sg.mejiar@alum.up.edu.pe',"1/01/2022-10:05")