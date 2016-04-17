## Source: http://docs.python-guide.org/en/latest/scenarios/scrape/

from lxml import html
import requests

## Retrieve the page with data
page = requests.get('http://econpy.pythonanywhere.com/ex/001.html')
## (We need to use page.content rather than page.text because
## html.fromstring implicitly expects bytes as input.)
tree = html.fromstring(page.content)

#This will create a list of buyers:
buyers = tree.xpath('//div[@title="buyer-name"]/text()')
#This will create a list of prices
prices = tree.xpath('//span[@class="item-price"]/text()')

print 'Buyers: ', buyers
print 'Prices: ', prices


## Now write a loop to extract all the buyers and prices from various
## page and add to the current list.
