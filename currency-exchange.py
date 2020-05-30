import requests
import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders
import schedule
import time


def send_exchange_rate():
        api_key = '18538a940f80b6a9c509dbef'

    #Endpoint
    # GET https://v6.exchangerate-api.com/v6/YOUR-API-KEY/latest/USD

    currency = 'USD'

    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{currency}"

    r = requests.get(url)

    output = r.json()

    USD_code = output['base_code']

    conversation_rates = output['conversion_rates']
    usd = conversation_rates['USD']
    inr = conversation_rates['INR']

    if inr > 75 or inr <70:
        fromaddr = "senderEmail@service.com" #You might get an authentication error. You can go to https://stackoverflow.com/questions/16512592/login-credentials-not-working-with-gmail-smtp to fix the error.
        toaddr = "ReceiverEmail@service.com"
        password = "Enter Your Password Here"

        # instance of MIMEMultipart 
        msg = MIMEMultipart() 

        # storing the senders email address   
        msg['From'] = fromaddr 

        # storing the receivers email address  
        msg['To'] = toaddr 

        # storing the subject
        if inr > 75:
            msg['Subject'] = "Value of INR is more than 75"
            body = f"Value of INR is more than 75. Today's rate is {inr}"
        else:
            msg['Subject'] = "Value of INR is less than 70"
            body = f"Value of INR is less than 70. Today's rate is {inr}"

        # string to store the body of the mail 
        

        # attach the body with the msg instance 
        msg.attach(MIMEText(body, 'plain')) 


        # creates SMTP session 
        s = smtplib.SMTP('smtp.gmail.com', 587) 

        # start TLS for security 
        s.starttls() 

        # Authentication 
        s.login(fromaddr, password) 

        # Converts the Multipart msg into a string 
        text = msg.as_string() 

        # sending the mail 
        s.sendmail(fromaddr, toaddr, text) 

        # terminating the session 
        s.quit() 
    else:
        msg['Subject'] = "Today's INR value"
        body = f"Today's rate is {inr}"


schedule.every().day.at("07:00").do(send_exchange_rate)

while True:
    schedule.run_pending()
    time.sleep(1)