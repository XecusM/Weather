import requests
from bs4 import BeautifulSoup as soup
import time
import pandas as pd

def Countries():

    try :
        url = requests.get('https://www.weather-forecast.com/countries')
    except:
        print('Error in reading page!')
        quit()

    page = soup(url.content, 'html.parser')

    containers = page.findAll('div',{'class':'mapctrytab-cont'})

    countries = pd.DataFrame(columns=['country','link'])
    counter = 0
    for con in containers:
        links = con.findAll('a')
        for link in links:
            countries.loc[counter] = [link.text,'https://www.weather-forecast.com{0}'.format(link['href'])]
            counter += 1

    print('Countries Page has scrapped successfully')
    return countries

def Cities(country):
    cities = pd.DataFrame(columns=['city','link'])
    url = requests.get(country['link'])
    page = soup(url.content, 'html.parser')
    section = page.findAll('section',{'class':'b-wrapper'})
    links = section[0].findAll('a')
    counter = 0
    for link in links:
        cities.loc[counter] = [link.text,'https://www.weather-forecast.com{0}'.format(link['href'])]
        counter +=1

    print('Cities Page has scrapped successfully')
    return cities

def City(city):
    weather = pd.DataFrame(columns=['days','dates','time','HighTemp','LowTemp'])
    url = requests.get(city['link'])
    page = soup(url.content, 'html.parser')

    days = page.findAll('span',{'class':'b-forecast__table-days-name'})
    times = ['AM','PM','NIGHT']
    dates = page.findAll('span',{'class':'b-forecast__table-days-date'})
    temps = page.findAll('span',{'class':'temp b-forecast__table-value'})

    for count in range(len(days)):
        for wcount in  range(len(times)):
            mycount = (count*3)+wcount
            weather.loc[mycount]=[
                    days[count].text,
                    dates[count].text,
                    times[wcount],
                    temps[mycount].text,
                    temps[mycount+len(days)*3].text
                    ]

    print('Weather Page has scrapped successfully')
    return weather

def main():
    countries = Countries()
    country = {'country':countries['country'][0],'link':countries['link'][0]}
    time.sleep(5)
    cities = Cities(country)
    city = {'city':cities['city'][0],'link':cities['link'][0]}
    time.sleep(5)
    weather = City(city)


if __name__ == '__main__':
    main()
