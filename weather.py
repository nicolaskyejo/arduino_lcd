import serial
import requests
import bs4
import time


port = 'COM3'  # on Windows
url = 'https://supersaa.fi'  # default setting is 'Helsinki', to change location open url in web browser or send cookies

#TODO
# Replace web scraping with weather api


def serial_write(string):
    with serial.Serial(port) as ser:
        assert ser.name == port
        time.sleep(2)  # without this, serial write doesn't take place
        ser.write(string.encode('utf-8'))


def weather_scraper():
    r = requests.get(url)
    r.raise_for_status()

    soup = bs4.BeautifulSoup(r.text, 'lxml')
    weather = soup.find(class_='supers-forecast-lane-item-large supers-lane-header-next-hours')
    weather_top = list(weather.children)[1]
    weather_bottom = list(weather.children)[3]

    temperature = weather_top.find(class_='supers-current-temperature').get_text()
    wind_speed = weather_top.find(class_='supers-windspeed').get_text()
    feels_like = weather_bottom.find(class_='supers-temperature').find('span', 'supers-value').get_text()
    rain_probability = weather_bottom.find(class_='supers-probability-of-rain').find('span', 'supers-value').get_text()
    rain_amount = weather_bottom.find(class_='supers-rain-amount').find('span', 'supers-value').get_text()

    print(temperature, wind_speed, feels_like, rain_probability, rain_amount)  # debug
    current_time = time.strftime('%H:%M')
    string = f'Temp is {temperature}C/{feels_like}C at {current_time}'.replace('°', '')
    return string


if __name__ == '__main__':
    while True:
        serial_write(weather_scraper())
        time.sleep(60 * 60)  # better way is to use crontab in Linux or task scheduler in Windows