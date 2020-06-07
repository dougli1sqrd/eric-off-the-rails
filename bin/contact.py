#!/home/ericoff/env/bin/python3

import smtplib
import click

from email import message


@click.command()
@click.argument("f")
@click.option("--subject", "-s", required=True)
@click.option("--note", "-m", required=True)
def send_message(f, subject, note):

    m = message.EmailMessage()
    m.set_content(str(note))
    m["Subject"] = str(subject)
    m["From"] = str(f)
    m["To"] = "eric@ericofftherails.city"
    m.as_string()

    s = smtplib.SMTP(host="web.electricembers.net", port=25)
    print("made smpt object")
    s.send_message(m)
    print("sent")
    s.quit()


if __name__ == "__main__":
    send_message()
