import smtplib
from email.mime.text import MIMEText
import os

def send_mail(name, description, price, qty):
  port = 2525
  smtp_server = 'smtp.mailtrap.io'
  login = os.getenv('MAILTRAP_LOGIN')
  password = os.getenv('MAILTRAP_PASSWORD')
  message = f"<h3>New Feedback submission</h3><ul><li>Customer: {name}</li><li>Dealer: {description}</li><li>Rating: {price}</li><li>Comments: {qty}</li></ul>"

  sender_email = 'email@example.com'
  receiver_email = 'ryan.adaptivebiz@gmail.com'
  msg = MIMEText(message, 'html')
  msg['Subject'] = 'Python Project'
  msg['From'] = sender_email
  msg['To'] = receiver_email

  # Send email
  with smtplib.SMTP(smtp_server, port) as server:
    server.login(login, password)
    server.sendmail(sender_email, receiver_email, msg.as_string())