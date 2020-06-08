#!/home/ericoff/env/bin/python3

import smtplib
import mimetypes
import json
import cgitb
import cgi
import os

import email
from email import message

cgitb.enable()

def main():
    form = cgi.FieldStorage()
    name = form.getfirst("name", "No one")
    subject = form.getfirst("subject", "")
    from_email = form.getfirst("email", "")
    message = form.getfirst("message", "")

    if os.getenv("REQUEST_METHOD") == "POST":
        send_message(from_email, "{}: {}".format(name, subject), message)

    out(json.dumps({}), "json")


def send_message(f, subject, note):

    m = message.EmailMessage()
    m.set_content(str(note))
    m["Subject"] = str(subject)
    m["From"] = str(f)
    m["To"] = "eric@ericofftherails.city"
    m.as_string()
    s = smtplib.SMTP(host="web.electricembers.net", port=25)
    # print("made smpt object")
    s.send_message(m)
    # print("sent")
    s.quit()


def out(data: str, mime: str):
    mime_out = mimetypes.types_map.get(mime, "text/plain")
    print("Content-Type: {}\n".format(mime_out))
    print(data)


if __name__ == "__main__":
    main()
