import requests
import folium
import datetime
from email.message import EmailMessage
import ssl
import smtplib

# Email configuration
email_sender = 'hassantarhini45@gmail.com'
email_pass = "xang psot mbyy qpky"  # Update with your actual password
email_receiver2 = 'hassantarhine45@gmail.com'

subject = 'Location Coordinates'
body = "Your child is currently suffering from an epileptic attack. Their current location is:\n"

def send_email(lat, long ,  email_receiver):
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body + f"Latitude: {lat}, Longitude: {long}")

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_pass)
        smtp.sendmail(email_sender, email_receiver, em.as_string())

# this method will return us our actual coordinates
# using our IP address
def location_coordinates():
    try:
        response = requests.get('https://ipinfo.io')
        data = response.json()
        loc = data['loc'].split(',')
        lat, long = float(loc[0]), float(loc[1])
        city = data.get('city', 'Unknown')
        state = data.get('region', 'Unknown')
        return lat, long, city, state
    except Exception as e:
        print("Error fetching location:", e)
        return False

# this method will fetch our coordinates and create an HTML file
# of the map
def gps_locator():
    obj = folium.Map(location=[0, 0], zoom_start=2)
    
    try:
        lat, long, city, state = location_coordinates()
        print("You are in {},{}".format(city, state))
        print("Your latitude = {} and longitude = {}".format(lat, long))
        folium.Marker([lat, long], popup='Current Location').add_to(obj)
        
        send_email(lat, long)
        print("Location coordinates sent via email.")

        file_name = "C:/screengfg/Location" + str(datetime.date.today()) + ".html"
        obj.save(file_name)

        return file_name
    except Exception as e:
        print("Error:", e)
        return False


