import requests
from lxml import html  
import csv,os,json
import requests
import re
from time import sleep
import pandas as pd
import random
try:
    new_data = pd.DataFrame()
    url = 'https://www.amazon.com/s?keywords=jewelry'
    user_agent_list = ['Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) \
                        Gecko/20100101 Firefox/61.0',
                       'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
                        (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36',
                       'Mozilla/5.0 (X11; Linux x86_64; rv:61.0) \
                        Gecko/20100101 Firefox/61.0',
                       'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                        AppleWebKit/537.36 (KHTML, like Gecko) \
                        Chrome/60.0.3112.113 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                        AppleWebKit/537.36 (KHTML, like Gecko) \
                        Chrome/63.0.3239.132 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                        AppleWebKit/537.36 (KHTML, like Gecko) \
                        Chrome/66.0.3359.117 Safari/537.36',
                       'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) \
                        AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 \
                        Safari/603.3.8',
                       'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) \
                        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 \
                        Safari/537.36',
                       'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) \
                        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 \
                        Safari/537.36']
    # a = random.choice(user_agent_list)
    page = requests.get(url, headers={'User-Agent':random.choice(user_agent_list)}).content
    page = page.decode('utf-8')
    
    pattern = re.compile(r"/dp/(?P<asin>\w+).*")
    asin =  re.findall(pattern,page)

    for i in set(asin):
        page = requests.get('http://www.amazon.com/dp/'+str(i), headers={'User-Agent':random.choice(user_agent_list)})
        doc = html.fromstring(page.content)
        XPATH_NAME = '//*[@id="productTitle"]//text()'
        XPATH_SELLER = '//*[@id="sellerProfileTriggerId"]//text()'
        XPATH_ORIGINAL_PRICE = '//*[@id="priceblock_ourprice"]//text()'
        RAW_NAME = doc.xpath(XPATH_NAME)
        RAW_SELLER = doc.xpath(XPATH_SELLER)
        RAW_ORIGINAL_PRICE = doc.xpath(XPATH_ORIGINAL_PRICE)
        XPATH_IMAGE = '//div[@id="imgTagWrapperId"]/img/@data-old-hires'
        RAW_IMAGE = doc.xpath(XPATH_IMAGE)
        RAW_IMAGE

#             print(RAW_NAME,RAW_SELLER,RAW_ORIGINAL_PRICE)
        NAME = ' '.join(''.join(RAW_NAME).split()) if RAW_NAME else None
        SELLER = '  '.join([i.strip() for i in RAW_SELLER]) if RAW_SELLER else None
        ORIGINAL_PRICE = ' '.join(RAW_ORIGINAL_PRICE).strip() if RAW_ORIGINAL_PRICE else None
        RAW_IMAGE = ''.join(RAW_IMAGE) if len(RAW_IMAGE)>0 else None
#             print(NAME,SELLER,ORIGINAL_PRICE)
        data = pd.DataFrame([[NAME,SELLER,ORIGINAL_PRICE,RAW_IMAGE]],columns = ['NAME','SELLER','ORIGINAL_PRICE','IMAGE_URL'])
        new_data = new_data.append(data,sort=False)
        new_data = new_data.drop_duplicates()
    #     new_data = pd.concat(data)
        print(new_data)
    c+=1
    print(c)
    
#         print(new_data.head())
except Exception as e:
    print(e)
new_data.to_csv('/home/ai101/Documents/Rushiket/amazon.csv',index=False)    