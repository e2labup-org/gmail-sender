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

    def message_to_send(self,tipo_de_correo):

        mimeMessage1 = MIMEMultipart()
        mimeMessage1['to'] = self.email # Destinatario 

        if tipo_de_correo == 'Personalizado': #Mail con el Link para la sesión

            mimeMessage1['subject'] = 'E2LABUP | Link Experimento'
            mimeMessage1.attach(MIMEText(open(Path("Message_personal.html")).read().format(self.nombres,self.apellidos,self.label), 'html'))

        elif tipo_de_correo == 'Recordatorio': #Recordatorio 30 min antes
            
            mimeMessage1['subject'] = 'E2LABUP | Recordatorio sesión experimental en línea HOY'
            mimeMessage1.attach(MIMEText(open(Path("Message_reminder.html")).read().format(self.nombres,self.apellidos), 'html'))

        else: #Fin del experimento

            mimeMessage1['subject'] = 'E2LABUP | Fin Experimento de Hoy'
            mimeMessage1.attach(MIMEText(open(Path("Message_final.html")).read().format(self.nombres,self.apellidos), 'html'))
    
        raw_string1 = base64.urlsafe_b64encode(mimeMessage1.as_bytes()).decode()

        service.users().messages().send(userId='me', body={'raw': raw_string1}).execute() #envia el correo
        print("Correo enviado para: {} {} al {}".format(self.nombres,self.apellidos,self.email))

    def send_email(self,fecha,tipo_de_correo):

        fecha = datetime.strptime(fecha, '%d/%m/%Y-%H:%M')
        sched.add_job(self.message_to_send, 'date', run_date=((fecha)), args=[tipo_de_correo])
        print("Preparando correo para: {} {} al {}".format(self.nombres,self.apellidos,self.email))

###########################################################################

class E2lab_email(): 

    def __init__(self,data,fecha):
        self.data = data
        self.fecha = fecha

    def send_emails(self,tipo_de_correo):

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
                ).send_email(self.fecha,tipo_de_correo)

session = E2lab_email(
                data = 'test.csv',
                fecha = "3/01/2022-18:12" #dd/mm/aaaa-hh:mm
                ) 
session.send_emails(tipo_de_correo='Recordatorio') 

sched.start() #no escribir nada despues de esto