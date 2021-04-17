import urllib
import urllib.request
from bs4 import BeautifulSoup


def download(image1, image2):
    # download zerodium prices image
    print('Downloading prices image..')
    imageFile = open('/var/www/html/saint/markets/zerodium_prices.png', 'wb')
    imageFile.write(urllib.request.urlopen(image1).read())
    imageFile.close()

    # download zerodium prices mobile image
    print('Downloading prices mobile image..')
    imageFile = open('/var/www/html/saint/markets/zerodium_prices_mobiles.png', 'wb')
    imageFile.write(urllib.request.urlopen(image2).read())
    imageFile.close()


if __name__ == '__main__':

    # URLS
    prices = 'https://zerodium.com/images/zerodium_prices.png'
    pricesMobile = 'https://zerodium.com/images/zerodium_prices_mobiles.png'

    # running function
    download(prices, pricesMobile)

    print('Images have successfully downloaded to the server!')
