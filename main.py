import requests
from datetime import datetime
import smtplib

YOUR_LAT = 51.507351  # Your latitude
YOUR_LONG = -0.127758  # Your longitude
YOUR_EMAIL = ""  # Your email
YOUR_PASSWORD = ""  # Your password
RECEIVER_EMAIL = ""  # Email of person you want to receive the mail


def iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    if abs(iss_latitude - YOUR_LAT) <= 5 and abs(iss_longitude - YOUR_LONG) <= 5:
        return True
    else:
        return False


def is_night():
    parameters = {
        "lat": YOUR_LAT,
        "lng": YOUR_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now()
    current_hour = time_now.hour
    print(current_hour)

    if current_hour >= sunset:
        return True
    else:
        return False


if iss_overhead() and is_night():
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(YOUR_EMAIL, YOUR_PASSWORD)
        connection.sendmail(from_addr=YOUR_EMAIL, to_addrs=RECEIVER_EMAIL,
                            msg="Subj: ISS is Overhead!\n\nThe ISS is over your head now. Go outside and look up!")


