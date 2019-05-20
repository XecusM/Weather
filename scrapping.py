import requests
from bs4 import BeautifulSoup as soup
import time
import pandas as pd

def Countries():
    '''
    Function for scrapping list of counties available on th web.
    '''
    #Connect to the web-site and scrapping all countries data
    try :
        url = requests.get('https://www.weather-forecast.com/countries')
    except:
        print('Error in reading page!')
        quit()
    #get all contents
    page = soup(url.content, 'html.parser')
    # Find countries div
    containers = page.findAll('div',{'class':'mapctrytab-cont'})
    # intiate countries dataframe
    countries = pd.DataFrame(columns=['country','link'])
    # help counter for getting links
    counter = 0
    # get all names and links for every country
    for con in containers:
        links = con.findAll('a')
        for link in links:
            # Add country name and link to dataframe
            countries.loc[counter] = [link.text,'https://www.weather-forecast.com{0}'.format(link['href'])]
            # counter for the next link
            counter += 1

    print('Countries Page has scrapped successfully')
    # return counteries dataframe
    return countries

def Cities(country):
    '''
    Function for scrapping list of cities available on the web
    for the selected country
    '''
    # initiate dataframe for cities data
    cities = pd.DataFrame(columns=['city','link'])
    #Connect to the web-site and scrapping cities data for selected country
    url = requests.get(country['link'])
    #get all contents
    page = soup(url.content, 'html.parser')
    # Find cities section
    section = page.findAll('section',{'class':'b-wrapper'})
    # get all cities links
    links = section[0].findAll('a')
    # help counter for getting links
    counter = 0
    # get all names and links for every city
    for link in links:
        # Add city name and link to dataframe
        cities.loc[counter] = [link.text,'https://www.weather-forecast.com{0}'.format(link['href'])]
        counter +=1

    print('Cities Page has scrapped successfully')
    # return cities dataframe
    return cities

def City(city):
    '''
    Function for scrapping weather details for the selected city
    '''
    # initiate dataframe for weather data
    weather = pd.DataFrame(columns=['days','dates','time','HighTemp','LowTemp'])
    #Connect to the web-site and scrapping weather data for selected city
    url = requests.get(city['link'])
    #get all contents
    page = soup(url.content, 'html.parser')
    # get spans for days names
    days = page.findAll('span',{'class':'b-forecast__table-days-name'})
    # initiate available times
    times = ['AM','PM','NIGHT']
    # get spans for days dates
    dates = page.findAll('span',{'class':'b-forecast__table-days-date'})
    # get spans for temperatures
    temps = page.findAll('span',{'class':'temp b-forecast__table-value'})

    # get all days names and dates
    for count in range(len(days)):
        # get all temperatures for all days and times [High Temperatures, Low Temperatures]
        for wcount in  range(len(times)):
            # get temperatures for count day
            mycount = (count*3)+wcount
            weather.loc[mycount]=[
                    days[count].text,
                    dates[count].text,
                    times[wcount],
                    temps[mycount].text,
                    temps[mycount+len(days)*3].text #get the low temperatures
                    ]

    print('Weather Page has scrapped successfully')
    # return weather dataframe
    return weather

def main():
    '''
    This main function to test the script alone
    '''
    # scrapping countries
    countries = Countries()
    # select the first country
    country = {'country':countries['country'][0],'link':countries['link'][0]}
    # pause for one second to avoid web blocking
    time.sleep(1)
    # scrapping cities for selected country
    cities = Cities(country)
    # select the first city
    city = {'city':cities['city'][0],'link':cities['link'][0]}
    # pause for one second to avoid web blocking
    time.sleep(1)
    # scrapping weather for selected city
    weather = City(city)


if __name__ == '__main__':
    main()
