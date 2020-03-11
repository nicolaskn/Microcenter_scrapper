__author__ = 'Nicolas Keeton'


class Const(object):


    '''Rename columns'''
    LABEL_NAME_CHANGE = {'name': 'Product Name',  'prices': 'Price', 'instore': 'Only Instore', 'sku': 'SKU #' }


    '''Email related'''
    RECIVING_EMAIL = 'XXXXXXX'
    SENDER_EMAIL = 'XXXXXX@support.org'
    SUBJECT_OF_MAIL = 'Microcenter Price Chart ( {}, {}, {} )'


    ''' Stores and their id'''

    STORES = {'065' : 'DULUTH_GA' ,
              '041': 'MARIETTA_GA' }



    '''CATEGORY'''

    CATEGORIES = {'4294964325' : 'Computers' ,
    '4294967288' : 'Laptop'                ,
    '4294899875' : 'iPads'   }


    '''URLS'''

    COMPUTER_CATEGORY_URL ="https://www.microcenter.com/search/search_results.aspx?storeID=065&Change+Store=Change+Store&N=4294964325&NTK=all&NR=&sku_list=&cat=Computers-:-MicroCenter"
    BASE_SEARCH_URL = "https://www.microcenter.com/search/search_results.aspx?storeID={}&Change+" \
                      "Store=Change+Store&N={}"



    '''API KEYS'''
    SEND_GRID_API_KEY = 'SG.XXXXXXXXXXXXXXXX'

    USA_DATE = '%m-%d-%Y'
    ASIA_DATE = '%Y-%m-%d'


