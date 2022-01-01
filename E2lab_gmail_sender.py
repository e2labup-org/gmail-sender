from Google_Module import Create_Service
import base64
from apscheduler.schedulers.blocking import BlockingScheduler
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

CLIENT_SECRET_FILE = 'client_secret_2.json'
API_NAME = 'gmail'
API_VERSION = 'v1'
SCOPES = ['https://mail.google.com/']

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
sched = BlockingScheduler()

class Participant():

    def __init__(self,apellidos,nombre,email,fecha):
        self.apellidos = apellidos
        self.nombre = nombre
        self.email = email
        self.fecha = fecha 

    def message(self,message):

        message = '''
                <!DOCTYPE html>
                <html>
                    <body>
                        <h1 style="color:SlateGray;">Hola {} {}, te escribimos del E2labUP</h1>
                    </body>
                </html>
            '''.format(self.nombre,self.apellidos)  

        mimeMessage1 = MIMEMultipart()
        mimeMessage1['to'] = self.email # Destinatario (Cuentas de correos)
        mimeMessage1['subject'] = 'Mensaje Prueba del E2labUP'
        mimeMessage1.attach(MIMEText(message, 'html'))
        raw_string1 = base64.urlsafe_b64encode(mimeMessage1.as_bytes()).decode()

        message1 = service.users().messages().send(userId='me', body={'raw': raw_string1}).execute()
        
        global running
        running = False

        print(message1)
        print("El correo de prueba para {} {} acaba de ser enviado al {} ".format(self.nombre,self.apellidos,self.email))
       
    def send_email(self):

        self.fecha = datetime.strptime(self.fecha, '%d/%m/%Y-%H:%M')
        sched.add_job(self.message, 'date', run_date=((self.fecha)), args=['text'])
        print("El correo de prueba será enviado para {} {} al {} en {}".format(self.nombre,self.apellidos,self.email,self.fecha))

participante = Participant('Mejia Ramos','Sergio Gonzalo','sg.mejiar@alum.up.edu.pe',"1/01/2022-11:56")
participante2 = Participant('Mejia Ramitos','Sergio Gonzalo','sg.mejiar@up.edu.pe',"1/01/2022-11:57")
participante.send_email()
participante2.send_email() 

sched.start()