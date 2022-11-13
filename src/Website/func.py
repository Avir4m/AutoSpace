import smtplib
import uuid
from email.message import EmailMessage
from PIL import Image
from werkzeug.utils import secure_filename
import os
from flask import current_app



ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'mp4'}

def send_email(email_recipient, title, text):
    with open('.venv/config.txt', 'r') as f:
        content = f.readlines()
        EMAIL_SENDER = content[1]
        PASSWORD = content[4]
        f.close()
       
        msg = EmailMessage()
        msg['Subject'] = title
        msg['From'] = EMAIL_SENDER
        msg['To'] = email_recipient
        
        msg.set_content(title)
        
        msg.add_alternative(f"""\
        <!DOCTYPE html>
                <html>
                    <head>
                        <meta charset="utf-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1">
                        <link 
                        href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0/dist/css/bootstrap.min.css" 
                        rel="stylesheet" 
                        integrity="sha384-gH2yIJqKdNHPEq0n4Mqa/HGKIhSkIHeL5AyhkYV8i59U5AR6csBvApHHNl/vI1Bx" 
                        crossorigin="anonymous">
                    </head>
                    <body>
                        <h1 align="center">{title}</h1>
                        <p align="center">{text}</p>
                        <script 
                        src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0/dist/js/bootstrap.bundle.min.js" 
                        integrity="sha384-A3rJD856KowSb7dwlZdYEkO39Gagi7vIsF0jrRAoQmDKKtQBHUuLZ9AsSv4jD4Xa" 
                        crossorigin="anonymous"></script>


                        <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.5/dist/umd/popper.min.js" 
                        integrity="sha384-Xe+8cL9oJa6tN/veChSP7q+mnSPaj5Bcu9mPX5F5xIGE0DVittaqT5lorf0EI7Vk" 
                        crossorigin="anonymous"></script>

                        
                        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0/dist/js/bootstrap.min.js" 
                        integrity="sha384-ODmDIVzN+pFdexxHEHFBQH3/9/vQ9uori45z4JjnFsRydbmQbmL5t1tQ0culUzyK" 
                        crossorigin="anonymous"></script>
                    </body>
                </html>
        """, subtype='html')
        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.ehlo()
            smtp.login(EMAIL_SENDER, PASSWORD)
            smtp.send_message(msg)
            smtp.close()
        
        f.close()
    
    
def get_secret_key():
    with open(".venv/config.txt", "r") as f:
        SECRET_KEY = f.readlines()
        f.close()
    return SECRET_KEY[7]


def create_url(type):  
    url = uuid.uuid4().hex
    model = type.query.filter_by(url=url).first()
    if model:
        create_url(type)
    else:
        return url


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
           
def unique_filename(filename, type):
    new_filename = filename + '_' + uuid.uuid4().hex
    picture = type.query.filter_by(picture=new_filename).first()
    if picture:
        unique_filename(filename)
    else:
        return new_filename
        
def upload_file(file, type):
    if file and allowed_file(file.filename):
        filename, ext = secure_filename(file.filename).split('.')
        filename = unique_filename(filename, type) + '.' + ext
        file.save(os.path.join(os.getcwd() + current_app.config['UPLOAD_FOLDER'] + f'/{type.lower()}s/', filename))
        return filename
    else:
        return None