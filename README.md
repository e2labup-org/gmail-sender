Título del programa: Envío de correos de Gmail a través de python

Descripción general: Este proyecto fue creado para generar correos y programar sus envíos a través de python y usando Gmail API. 

Descripción del Script: 
- Incialmente se muestran los módulos y librerías usados para la creación del servidor de Google y para el envío de correos. 
- Primera parte: creación del módulo de Google. En esta parte, se establecen las variables que receptan la información del API desde el archivo de pickle (token).
  CLIENT_SECRET_FILE alberga el archivo JSON descargado desde Google Cloud Project (client_secret_2.json)
- En la parte denominada "Input de usuario", se pide al usuario ingresar la fecha y hora de inicio del experimento así como la duración del mismo bajo el formato que se pide. 
  De la misma forma, si el usuario ingresa bajo un formato incorrecto, se notificará para que vuelva a ingresarlo. 
- Después, se generan tres funciones my_job1, my_job2 y my_job3 contienen el mensaje en formato html. También contiene el formato del envío del mensaje por correo como destinatario, sujeto, etc. 
  Para ello se crean 3 diferentes mensajes: uno que se envía 30 minutos antes del experimento, otro que se envía 1 minutos antes del experimento y otro que se envía al finalizar el experimento. 
- En la última parte denominada "Horas de envío", a través del uso de scheduler, se establecen los minutos previos o posteriores al inicio del experimento en los que se envían los tres correos. 

Requerimientos:
- Python (versión usada 3.7.7) 

Módulos y Librerías de Python:
- APScheduler==3.7.0
- Datetime==4.3
- google-api-python-client==2.7.0
- google-auth==1.30.1
- google-auth-httplib2==0.1.0
- google-auth-oauthlib==0.4.4

Enable Gmail API:
1. Ingresar a console.cloud.google.com desde una cuenta de Gmail.
2. Desde APIs and Services, buscar GMAIL API y click en Manage this API.

Create Google Cloud Project and download Client File:
1. Desde console.cloud.google.com, ir a "select a project" y crear un proyecto nuevo.
2. Ir a la barra lateral izquierda y click en APIs and Services, desde ahí, click en Credentials.
3. Para crear una credencial, verificar que se está en el proyecto creado. Dirigirse hacia "+Create Credentials". 
4. Hacer click en "OAuth Client ID", luego "Configure consent screen". Configurar el tipo de usuario a "External" y crear la credencial. 
5. En la plataforma de "OAuth consent screen", configurar el nombre de la aplicación del usuario. En Test Users, se añadirá la 
   cuenta de correo desde la que se desea enviar los mensajes para que sea habilitada.Terminada la configuración, se aceptan los cambios.
6. Se vuelve a ingresar a Credentials para crear OAtuh client ID, en la barra de selección "Application type", se elige la opción "Desktop type"
7. Se regresa a la página de credentials y aparecerá un archivoen el área de OAuth 2.0 Client IDs. El archivo se llamará por defecto "Desktop client 1" y
   deberá ser descargado en la carpeta en la que se encuentra el script del programa. 
8. Este archivo JSON deberá ser renombrado como "client_secret_2.json"

Creación del token:
1. Se selecciona la parte del script denominada "Segunda parte: creación del token"
2. Se generará un link que nos conducirá a elegir desde qué cuenta queremos enviar los correos
3. Como la cuenta ya fue verficada desde "OAuth consent screen", se deberá ir a las opciones avanzadas que ofrece Google Gmail
   para finalmente garantizar el permiso de Google API a la cuenta. 
4. Aparecerá un mensaje indicando que ya fue habilitado la cuenta para enviar correos y automáticamente se descargará un archivo pickle que contendrá el token. 
   Este se almacenará en la carpeta del script del programa. 

Funcionalidad:  
Para ejecutar este programa, al correrse el script, se pide al usuario ingresar la fecha y hora del experimento y debe ser ingresado bajo el siguiente formato: dd/mm/yyyy-hh:mm
A partir de ello, se muestra la fecha y hora de envío de cada uno de los tres mensajes. Y a medida que se cumpla el tiempo establecido, se van enviando los mensajes a los correos destinatarios de Gmail. 
