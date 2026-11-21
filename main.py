# To run and test the code you need to update 4 places:
# 1. Change MY_EMAIL/MY_PASSWORD to your own details.
# 2. Go to your email provider and make it allow less secure apps.
# 3. Update the SMTP ADDRESS to match your email provider.
# See the solution video in the 100 Days of Python Course for explainations.

from datetime import datetime
import pandas
import requests
import random
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# import os and use it to get the Github repository secrets
MY_EMAIL = os.environ.get("MY_EMAIL")
MY_PASSWORD = os.environ.get("MY_PASSWORD")

MY_LAT  = 20.906389 # Your latitude
MY_LONG = -103.976112 # Your longitude

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude =  float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])

#print(iss_latitude, iss_longitude)

#Your position is within +5 or -5 degrees of the ISS position.

parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}
#https://api.sunrise-sunset.org/v2?lat=20.906389&lng=-103.976112
response = requests.get(f"https://api.sunrise-sunset.org/v2?lat={MY_LAT}&lng={MY_LONG}")
response.raise_for_status()
data = response.json()
#print(data)

sunrise = int(data["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["sunset"].split("T")[1].split(":")[0])
#print(sunrise, sunset)
time_now = datetime.now()
#print(time_now)

#If the ISS is close to my current position
ahora = str(time_now).split(" ")[1].split(":")[0]

my_email = MY_EMAIL
password = MY_PASSWORD
msg = MIMEMultipart()
msg['From'] = my_email  # CRITICAL: Must match YAHOO_EMAIL exactly!
msg['To'] = my_email

if (MY_LAT-5 < iss_latitude < MY_LAT + 5) and (MY_LONG - 5 < iss_longitude < MY_LONG + 5):
    if int(sunset) <= int(ahora) or int(ahora) <= int(sunrise):
        #print("la ISS es visible")
        msg['Subject'] = " ISS aligned "
        with smtplib.SMTP('smtp.mail.yahoo.com', 587) as connection:
            #msg['Cc'] = my_email

            x = f"Voltea hacia el cielo, La ISS es visible -> lat: {iss_latitude}, lng: {iss_longitude}"
            msg.attach(MIMEText(x, 'plain'))

            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.send_message(msg)
else:
    msg['Subject'] = " ISS not aligned "
    with smtplib.SMTP('smtp.mail.yahoo.com', 587) as connection:
        x = f"""El script corrio, pero la ISS No es visible.
            ISS coords:
                lat: {iss_latitude} \t lng: {iss_longitude}\n 
            Tus coords:
                lat: {MY_LAT} \t lng: {MY_LONG}"""
        msg.attach(MIMEText(x, 'plain'))
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.send_message(msg)
       

        
        #connection.sendmail(from_addr=MY_EMAIL, to_addrs=birthday_person["email"], msg=f"Subject:Happy Birthday!\n\n{contents}")
