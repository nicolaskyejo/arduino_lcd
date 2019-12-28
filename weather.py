import serial
import requests
import bs4
import time


port = 'COM3'  # on Windows
url = 'https://supersaa.fi'  # default setting is 'Helsinki', to change location open url in web browser or send cookies


with serial.Serial(port) as ser:
    assert ser.name == port
    r = requests.get(url)
    r.raise_for_status()

    soup = bs4.BeautifulSoup(r.text, 'lxml')
    weather = soup.find(class_='supers-forecast-lane-item-large supers-lane-header-next-hours')
    weather_top = list(weather.children)[1]
    weather_bottom = list(weather.children)[3]
    temperature = weather_top.find(class_='supers-current-temperature').get_text()
    wind = weather_top.find(class_='supers-windspeed').get_text()
    feels_like = weather_bottom.find(class_='supers-temperature').find('span', 'supers-value').get_text()
    rain_probability = weather_bottom.find(class_='supers-probability-of-rain').find('span', 'supers-value').get_text()
    rain_amount = weather_bottom.find(class_='supers-rain-amount').find('span', 'supers-value').get_text()

    print(temperature, wind, feels_like, rain_probability, rain_amount)
    time.sleep(2)  # without this, serial write doesn't take place
    string = f'temp is {temperature}C, feels like {feels_like}C'.replace('°', '')
    ser.write(string.encode())
