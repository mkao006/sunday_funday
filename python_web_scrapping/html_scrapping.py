## 
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

## Define the function to get buyers so we can use it to extract the
## buyers for all the pages.
def get_buyers(page):
    page = requests.get(page)
    tree = html.fromstring(page.content)
    buyers = tree.xpath('//div[@title="buyer-name"]/text()')
    return buyers

## Testing the function
page1_buyers = get_buyers('http://econpy.pythonanywhere.com/ex/001.html')


## Now write a loop to extract all the buyers and prices from various
## page and add to the current list.

## However this does not get the link of the page we are currently on.
other_pages = tree.xpath("//a/@href")

## So we extend the original list with the buyers returned from other
## page
[page1_buyers.extend(get_buyers(page)) for page in other_pages]

## This is the full unique list of buyers
print(set(page1_buyers))


## Lets try scrap all the python codes
page = requests.get('http://docs.python-guide.org/en/latest/scenarios/scrape/')
tree = html.fromstring(page.content)

python_blocks = tree.xpath('//div[@class="highlight-python"]')

def join_codes(list_of_string):
    codes_only = [code for code in list_of_string if not code.startswith("#")]
    return(" ".join(codes_only))


## Need to find how to do line break and also when to include space
## when join. This should be included in the class of the span, but I
## couldn't obtain the detail of the class.
python_codes = [join_codes(code_list) for code_list in [x.xpath('.//span/text()') for x in python_blocks]]
