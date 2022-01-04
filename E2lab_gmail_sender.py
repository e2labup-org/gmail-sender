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

class Participant():

    def __init__(self,apellidos,nombres,email,telefono,label):
        self.apellidos = apellidos
        self.nombres = nombres
        self.email = email 
        self.telefono = telefono
        self.label = label

    def message_to_send(self,mensaje,asunto):

        mimeMessage = MIMEMultipart()
        mimeMessage['to'] = self.email # Destinatario 
        mimeMessage['subject'] = asunto #asunto
        mimeMessage.attach(MIMEText(mensaje.format(self.nombres,self.apellidos,self.label), 'html')) #mensaje

        raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()

        service.users().messages().send(userId='me', body={'raw': raw_string}).execute() #envia el correo
        print("Correo enviado para: {} {} | {}".format(self.nombres,self.apellidos,self.email))

    def send_email(self,fecha,mensaje,asunto):

        fecha = datetime.strptime(fecha, '%d/%m/%Y-%H:%M')
        sched.add_job(self.message_to_send, 'date', run_date=((fecha)), args=[mensaje,asunto])
        print("Preparando correo para: {} {} | {}".format(self.nombres,self.apellidos,self.email))

###########################################################################

class E2lab_email(): 

    def __init__(self,data,fecha,mensaje,asunto):
        self.data = data
        self.fecha = fecha
        self.mensaje = mensaje 
        self.asunto = asunto

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
                    label = new_data[4]
                ).send_email(self.fecha,self.mensaje,self.asunto)

session = E2lab_email(
                data = 'test.csv', #participantes correos/nombres/apellidos/telefono/label/etc
                fecha = "4/01/2022-12:16", #dd/mm/aaaa-hh:mm
                mensaje = open(Path("htmls/Message_reminder.html")).read(), #htmls/mensaje.html
                asunto = 'E2LABUP | Reminder' #asunto que sera enviado en el mail
            )

session.send_emails() #envia los mensajes

sched.start() #no escribir nada despues de esto