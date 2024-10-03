import smtplib
from email.mime.text import MIMEText
from utils.speak import speak
from utils.command_recognition import recognize_wake_and_command

def handle_email(command):
    subject = command.split("email")[1].strip()
    speak("Please speak the message.")
    message_body = recognize_wake_and_command(prompt="Listening for your message...")
    if message_body:
        send_email(subject, message_body)

def send_email(subject, body):
    sender = "your-email@example.com"
    recipient = "recipient@example.com"
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender, "your-password")
        server.sendmail(sender, recipient, msg.as_string())
        server.quit()
        speak("Email sent successfully.")
    except Exception as e:
        speak("Error sending email.")
