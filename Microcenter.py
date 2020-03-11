import requests
import pandas as pd
from bs4 import BeautifulSoup
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from datetime import datetime
from Const import Const

__author__ = 'Nicolas Keeton'

url = "https://www.microcenter.com/search/search_results.aspx?storeID=065&Change+Store=Change+Store&N=4294964325&NTK=all&NR=&sku_list=&cat=Computers-:-MicroCenter"
store_ids = ['065'], ['041']
category_ids = []

class microcenter:

    def __init__(self):
        self.Const = Const
        self.skus = []
        self.names = []
        self.prices = []
        self.instores = []
        # self.test_site(url)

    def search_store(self):
        for store_id in list(Const.STORES.keys()):
            for category_id in Const.CATEGORIES:
                url = Const.BASE_SEARCH_URL.format(store_id, category_id)
                price_df = self.scrape_site(url)
                self.send_email(price_df, store_id, category_id)

    def category_ids(self, store_id):
        #return list of all the category ids from page:
        #'https://www.microcenter.com/search/search_results.aspx?N=&Ntk=all&sortby=match&myStore=true&storeID={}&Change+"Store=Change+Store'.format(store_id)
        #need to scrap each page for their ids
        pass

    def scrape_site(self, url):
        r = requests.get(url)
        html_soup = BeautifulSoup(r.text, 'html.parser')


        #Get the max pages
        page_filters = html_soup.find('ul', class_='pages inline')
        pages_count = int(page_filters.find('li', {"style": "margin-left:5px;"}).text)


        # for page_number in range(1, pages_count):
        for page_number in range(1, 3):
            print(page_number)

            if page_number % 10 == 0:
                print(page_number)
            r = requests.get(url + ('&page={}'.format(page_number)))
            product_page = BeautifulSoup(r.text, 'html.parser')
            product_wrappers = product_page.find_all('li', class_='product_wrapper')
            self.get_from_pages(product_wrappers)

         # list to dictionary to dataframe
        dict = {"sku": self.skus , "name": self.names, "prices": self.prices, "instore": self.instores}
        df = pd.DataFrame(dict)

        df.rename(columns=Const.LABEL_NAME_CHANGE,  inplace=True)
        print('done')
        return df

    def get_from_pages(self, page_data):

        for product in page_data:
            item = product.find('div', class_= 'result_right')
            item_filtered = item.div.div.p.text
            sku_filtered = item_filtered.split(' ')
            self.skus.append(sku_filtered[1])

        #Get Price
            price_filtered = product.find('div', class_='price_wrapper')
            price_filtered = price_filtered.find('span', {"itemprop": 'price'})
            if price_filtered == None:
                price_filtered = product.find('span', {"class": 'no-price'})
                if "Add to Cart" in str(price_filtered.text):
                    self.prices.append(None)
            else:
                self.prices.append(str(price_filtered.text).replace('$', ''))



        #Get Name
            name_item_filtered = item.div.find('div', class_= 'pDescription compressedNormal3')
            if name_item_filtered == None:
                name_item_filtered = item.div.find('div', class_='pDescription compressedNormal4')
            if name_item_filtered == None:
                name_item_filtered = item.div.find('div', class_='pDescription compressedNormal2')
            name_item_filtered = name_item_filtered.div.h2.a.text
            name_item = name_item_filtered.split(';')
            self.names.append(name_item[0])

            # Determine if instore only
            instore_filter = item.find('div', {"class": "instore"})
            instore_value = str(instore_filter.text).strip('\n')

            if instore_value == 'In-Store Only':
                self.instores.append('Y')
            else:
                self.instores.append('N')

    def get_todays_date(self):

        today_date = datetime.today().strftime(Const.USA_DATE)
        return today_date

    def create_email_body(self, price_df, store_id, category_id):

            store_area = Const.STORES[store_id]
            category_name = Const.CATEGORIES[category_id]

            today_date = self.get_todays_date()
            message = Mail(
            from_email=Const.SENDER_EMAIL,
            to_emails=Const.RECIVING_EMAIL,
            subject=Const.SUBJECT_OF_MAIL.format(store_area, category_name, today_date),
            html_content='<strong>Current Prices</strong> <br> {}'.format(
                          price_df.to_html()))

            return message

    def send_email(self, price_df, store_id, category_id):
        message = self.create_email_body(price_df, store_id, category_id)

        try:
            sg = SendGridAPIClient(Const.SEND_GRID_API_KEY)
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
        except Exception as e:
            print(e.message)


m = microcenter()
m.search_store()
