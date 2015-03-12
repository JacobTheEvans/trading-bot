def shouldSell(orginal,current):
	#Min price for profit
	profit = .03
	if grossProfit(orginal,current) >= profit:
		return True
	else:
		return False

def grossProfit(orginal, current):
	temp = current - orginal
	result = float(temp) / float(current)
	return result
