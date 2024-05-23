import random
import string
from flask import current_app

from email.message import EmailMessage
from werkzeug.utils import secure_filename
from PIL import Image

import smtplib
import uuid
import os

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}


def send_email(email_recipient, title, text):
    EMAIL_SENDER, PASSWORD = "", ""


    msg = EmailMessage()
    msg["Subject"] = title
    msg["From"] = EMAIL_SENDER
    msg["To"] = email_recipient

    msg.set_content(title)

    msg.add_alternative(
        f"""\
    <!DOCTYPE html>
            <html>
                <head>
                    <meta charset="utf-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1">
                </head>
                <body>
                    <h1 align="center">{title}</h1>
                    <p align="center">{text}</p>
                </body>
            </html>
    """,
        subtype="html",
    )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.ehlo()
        smtp.login(EMAIL_SENDER, PASSWORD)
        smtp.send_message(msg)
        smtp.close()


def get_secret_key():
    SECRET_KEY = "SECRET_KEY"
    return SECRET_KEY

def generate_key(n):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=n))


def create_url(type):
    url = uuid.uuid4().hex
    model = type.query.filter_by(url=url).first()
    if model:
        create_url(type)
    else:
        return url


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def unique_filename(filename, type):
    new_filename = filename + "_" + uuid.uuid4().hex
    picture = type.query.filter_by(picture=new_filename).first()
    if picture:
        unique_filename(filename)
    else:
        return new_filename


def upload_file(file, type, path):
    path = os.path.join(os.getcwd() + current_app.config["UPLOAD_FOLDER"] + f"/{path}/")
    if file and allowed_file(file.filename):

        # Saving original file
        filename = secure_filename(file.filename)
        filename = unique_filename(filename, type) + ".jpg"
        file.save(os.path.join(path, filename))

        # Image resize, convertion and compression
        image = Image.open(os.path.join(path, filename)).convert("RGB")
        image.save(os.path.join(path, filename), optimize=True, quality=90)

        return filename
    else:
        return None

def create_folder(path):
    try:
        os.makedirs(path)
    except OSError as e:
        print(e)