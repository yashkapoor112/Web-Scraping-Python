from selenium import webdriver
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
import time
from matplotlib.backends.backend_pdf import PdfPages


class Hotels():
    def __init__(self):
        self.name = ""
        self.hotel_link = ""
        self.review_no = 0
        self.reviews = list()
        self.prices = None


class Prices():
    def __init__(self):
        self.save = ""
        self.maximum_price = ""
        self.lowest_price = ""
        self.lowest_price_site = ""
        self.other_sites_list = list()


def getHotelList(url, place):
    driver.get(url)

    input_place = driver.find_element_by_xpath('//*[@id="taplc_trip_search_home_default_0"]/div[2]/div[1]/div/span/input')
    input_place.send_keys(place)

    button = driver.find_element_by_xpath('//*[@id="SUBMIT_HOTELS"]')
    button.click()
   # html = requests.get(url).content
    time.sleep(5)
    soup =  BeautifulSoup(driver.page_source, "lxml")

    parent = soup.find('div', {'class': 'relWrap'})

    hotel_list = list()

    if (parent == None):
        print("Chrome Driver not responding")
        return hotel_list

    hotels = parent.find_all('div', {'class': 'rcol'})

    if (hotels == None):
        print("Chrome Driver not responding")
        return hotel_list

    for hotel in hotels:
        one_hotel = Hotels()
        hotel_detail = hotel.find('a', {'class': 'property_title'})
        if (hotel_detail != None):
            one_hotel.name = hotel_detail.text
            one_hotel.hotel_link = url + hotel_detail['href']

        # print(one_hotel.name+" "+one_hotel.hotel_link)

        price = Prices()
        price_details = hotel.find('div', {'class': 'priceBlock'})
        if (price_details != None):
            xthroughClass = price_details.find('div', {'class': 'xthroughBlock'})
            if (xthroughClass != None):
                price.save = xthroughClass.find('div', {'class': 'save'}).text
                price.maximum_price = xthroughClass.find('div', {'class': 'xthrough'}).text
            lowest_price = price_details.find('div', {'class': 'price'})
            if (lowest_price != None):
                price.lowest_price = lowest_price.text
            lowest_price_hotel = price_details.find('span', {'class': 'provider provName'})
            if (lowest_price_hotel != None):
                price.lowest_price_site = lowest_price_hotel.text

        extraHotels = list()
        extraHotelParent = hotel.find('div', {'class': 'text-links'})

        if (extraHotelParent == None):
            print("Chrome Driver not responding")
            return hotel_list

        extraHotelParentList = extraHotelParent.find_all('div', {
            'class': 'no_cpu offer text-link '}) + extraHotelParent.find_all('div', {
            'class': 'no_cpu offer text-link  unclickable'})

        for i in extraHotelParentList:
            extraHotelNameTemp = i.find('span', {'class': 'vendor'})
            if (extraHotelNameTemp != None):
                extraHotelsName = extraHotelNameTemp.text
            extraHotelPrice = 0
            extraHotelPriceTemp = i.find('span', {'class': 'price'})
            extraHotelParentTemp = i.find('span', {'class': 'price comparisonOffer'})
            if (extraHotelPriceTemp != None):
                extraHotelPrice = extraHotelPriceTemp.text
            elif (extraHotelParentTemp != None):
                extraHotelParent = extraHotelParentTemp.text
            extraHotels.append({extraHotelsName: extraHotelPrice})

            # print(extraHotelsName," : ",extraHotelPrice)

        price.other_sites_list = extraHotels
        one_hotel.prices = price
        hotel_list.append(one_hotel)
        print()
        # print(extraHotels)

        # print(price.save+" "+price.lowest_price+" "+price.lowest_price_site+" "+price.maximum_price+"\n")

    return hotel_list

pp = PdfPages('multipage.pdf')
def displayEverything(hotels):
    for hotel in hotels:
        objects = list()
        performance = list()

        print('\033[4m' + "NAME : ", hotel.name + '\033[0m')
        print("\nHOTEL LINK : ", hotel.hotel_link)

        prices = hotel.prices

        print("\nPRICE : ", prices.lowest_price, " by ", prices.lowest_price_site)

        print("\n" + prices.save)

        if (len(prices.maximum_price) != 0):
            print("\nMaximum price : ", prices.maximum_price)

        if (len(prices.lowest_price_site) != 0 and prices.lowest_price != 0):
            var1 = (prices.lowest_price.split(u'\xa0'))
            # print(int(prices.lowest_price.split()[1]))
            if (len(var1) > 1):
                var = var1[1].split(',')
                performance.append(int(var[0] + var[1]))
                objects.append(prices.lowest_price_site)
                # performance.append(1000)

        print("\n\n")

        othersites = prices.other_sites_list

        for i in othersites:
            for k in i:
                price = ""
                if (len(i[k]) != 0):
                    var = (i[k].split(u'\xa0')[1].split(','))
                    price = int(var[0] + var[1])
                objects.append(k)
                performance.append(price)

        y_pos = np.arange(len(objects))

        plt.barh(y_pos, performance, align='center', alpha=0.8, rasterized=True)
        plt.yticks(y_pos, objects)
        plt.xlabel('Prices')
        plt.ylabel('Website')
        plt.title(hotel.name)

        #pp = PdfPages('foo.pdf')
        #pp.savefig(plt)

        plt.savefig(pp, format='pdf')

        #plt.show()
        #f.savefig("foo.pdf", bbox_inches='tight')

        print("\n\n\n")



place = 'jaipur'

url = "https://www.tripadvisor.in/"


driver = webdriver.Chrome("C:\\Users\\admin\\Downloads\\chromedriver.exe")

hotels = getHotelList(url, place)
displayEverything(hotels)