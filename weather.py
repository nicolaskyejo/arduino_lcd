import serial
import requests
import bs4
import time


PORT = 'COM3'  # on Windows
URL = 'https://supersaa.fi'  # default setting is 'Helsinki', to change location open url in web browser, change location and send cookies
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
MINUTES = 60


# TODO
# Replace web scraping with weather api


def serial_write(text: str) -> None:
    with serial.Serial(PORT) as ser:
        assert ser.name == PORT
        time.sleep(2)  # without this, serial write doesn't take place
        ser.write(text.encode('utf-8'))


def weather_scraper() -> str:
    r = requests.get(URL, headers={'User-Agent': 'USER_AGENT'})
    if r.status_code == requests.codes.ok:
        soup = bs4.BeautifulSoup(r.text, 'lxml')
        weather = soup.find(class_='supers-forecast-lane-item-large supers-lane-header-next-hours')
        weather_top = list(weather.children)[1]
        weather_bottom = list(weather.children)[3]

        temperature = weather_top.find(class_='supers-current-temperature').get_text()
        wind_speed = weather_top.find(class_='supers-windspeed').get_text()
        feels_like = weather_bottom.find(class_='supers-temperature').find('span', 'supers-value').get_text()
        rain_probability = weather_bottom.find(class_='supers-probability-of-rain').find('span', 'supers-value').get_text()
        rain_amount = weather_bottom.find(class_='supers-rain-amount').find('span', 'supers-value').get_text()

        print(f'temp {temperature}/feels like {feels_like}, wind speed {wind_speed}, chance of rain {rain_probability}, rain fall {rain_amount} - {time.strftime("%A %H:%M")}')  # debug print
        current_time = time.strftime('%H:%M')
        text = f'Temp is {temperature}C/{feels_like}C at {current_time} -> {rain_probability}'.replace('°', '')
        return text
    else:
        return 'Weather data unavailable'


if __name__ == '__main__':
    while True:
        serial_write(weather_scraper())
        time.sleep(60 * MINUTES)  # better way is to use crontab in Linux or task scheduler in Windows