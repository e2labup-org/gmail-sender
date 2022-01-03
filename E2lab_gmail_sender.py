from Google_Module import Create_Service
import base64
from apscheduler.schedulers.blocking import BlockingScheduler
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from pathlib import Path


CLIENT_SECRET_FILE = 'client_secret_2.json'
API_NAME = 'gmail'
API_VERSION = 'v1'
SCOPES = ['https://mail.google.com/']

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
sched = BlockingScheduler()
message_reminder_file = open(Path("Message_reminder.html"))

class Participant():

    def __init__(self,apellidos,nombres,email,telefono,label,personalizado):
        self.apellidos = apellidos
        self.nombres = nombres
        self.email = email 
        self.telefono = telefono
        self.label = label
        self.personalizado = personalizado

    def message_to_send(self,mensaje):

        mensaje = ""

        if self.personalizado == True:

            mensaje = '''
            <!DOCTYPE html>
            <html>
                <body>
                    <h1>Hola {} {}</h1>
                    <p>
                        A continuacion te adjuntamos el link al cual debes acceder con la siguiente etiqueta:
                        {}
                    </p>
                </body>
            </html>
            '''.format(self.nombres,self.apellidos,self.label) 

        else:
            
            mensaje = message_reminder_file.read()

        mimeMessage1 = MIMEMultipart()
        mimeMessage1['to'] = self.email # Destinatario (Cuentas de correos)
        mimeMessage1['subject'] = 'Mensaje Prueba del E2labUP'
        mimeMessage1.attach(MIMEText(mensaje, 'html'))
        raw_string1 = base64.urlsafe_b64encode(mimeMessage1.as_bytes()).decode()

        service.users().messages().send(userId='me', body={'raw': raw_string1}).execute()
        
    def send_email(self,fecha):

        fecha = datetime.strptime(fecha, '%d/%m/%Y-%H:%M')
        sched.add_job(self.message_to_send, 'date', run_date=((fecha)), args=['text'])

###########################################################################

class E2lab_email(): 

    def __init__(self,data,fecha):
        self.data = data
        self.fecha = fecha

    def send_emails(self):
        ############ File Format #########
        # Apellidos | Nombres | Email | Telefono | Label 
        with open(self.data) as file: 
            for line in file: 
                new_data = line.split(';')
                Participant(
                    apellidos = new_data[0],
                    nombres = new_data[1],
                    email = new_data[2],
                    telefono = new_data[3],
                    label = new_data[4],
                    personalizado = False
                ).send_email(self.fecha)

session = E2lab_email('test.csv',"3/01/2022-12:26") #dd/mm/aaaa-hh:mm
session.send_emails() 

sched.start() #no escribir nada despues de esto