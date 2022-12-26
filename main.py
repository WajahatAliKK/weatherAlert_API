import os
import smtplib
import requests
from geopy.geocoders import Nominatim
from flask import Flask, request, jsonify

app = Flask(__name__)

# Replace with your API key
API_KEY = 'your_api_key'


@app.route('/weather-alert-subscription', methods=['POST'])
def subscribe_to_weather_alerts():
    # Extract the subscription details from the request payload
    data = request.get_json()
    email = data['email']
    location = data['location']
    weather_conditions = data['weather_conditions']

    # Consume the weather API to get the current weather at the specified location
    weather_data = get_current_weather(location)

    # Check if the current weather meets the specified conditions
    if weather_conditions_met(weather_data, weather_conditions):
        # Send an alert to the subscribed email address
        send_alert(email, weather_data)

    return jsonify({'status': 'success'})


def get_current_weather(location):
    # Make a request to the weather API to get the current weather at the specified location
    geolocator = Nominatim(user_agent="my-application")
    location = geolocator.geocode("New York, NY")
    lat = location.latitude
    lon = location.longitude
    url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}'
    response = requests.get(url)
    return response.json()


def weather_conditions_met(weather_data, weather_conditions):
    # Check if the current weather meets the specified conditions
    temperature = weather_data['main']['temp']
    if temperature < 0:
        return True
    return False


def send_alert(email, weather_data):
    # Send an alert to the subscribed email address with the current weather data
    # Replace these with your own email and SMTP server details
    sender_email = "sender@example.com"
    receiver_email = "receiver@example.com"
    smtp_server = "smtp.example.com"
    smtp_port = 587

    # Create the email message
    message = """\
    From: {sender_email}
    To: {receiver_email}
    Subject: Weather Alert

    There is a weather alert for your location. Please check the forecast for more information.
    """

    # Send the email
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login("sender@example.com", "sender_password")
    server.sendmail(sender_email, receiver_email, message)
    server.quit()


if __name__ == '__main__':
    app.run()
