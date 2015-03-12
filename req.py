import urllib2
import re

def priceRequest(symbol):
	url = "http://finance.google.com/finance?q=%s" % (symbol)
	content = urllib2.urlopen(url).read()
	result = re.search('span id="ref.*>(.*)<', content)

	return(float(result.group(1)))