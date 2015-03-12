import database as db
import thread
import em
import sell
import req
import sys
import datetime
import oss
import time


def listen():
	while True:
		time.sleep(0.002)
		raw_data = (em.read("serveremail@example.com","password"))

		if "," in raw_data:
			raw_data = raw_data.split(",")

		for i in raw_data:
			if "sold" in raw_data:
				db.removeQue(raw_data[0])
				db.removePrice(raw_data[0])
				break

		data = []
		for i in raw_data:
			i = i.replace("\n","")
			i = i.replace("\r","")
			data.append(i)

		item = data
		isPresent = False

		for i in db.loadPrices():
			if item[0] in i:
				isPresent = True

		for i in db.loadQue():
			if item[0] in i:
				isPresent = True

		if not isPresent:
			db.insertPrice(item[0],item[1])


def check():
	time.sleep(0.001)
	while True:
		for i in db.loadPrices():
			symbol = i.split(",")[0]
			now = datetime.datetime.now()
			price = i.split(",")[1]
			if sell.shouldSell(float(price),float(req.priceRequest(symbol))):
				em.send("serveremail@example.com","password","toAddres",("Should sell %s" % (symbol)))
				db.removePrice(symbol)
				db.insertQue(symbol,price,now.hour)



def que():
	time.sleep(1)
	while True:
		#check if day in que is not equal to today date if so add it to boughts
		data = db.loadQue()
		for i in data:
			past_time = i.split(",")[-1]
			if not (str(past_time) == str(datetime.datetime.now().hour)):
				db.insertPrice(i.split(",")[0],i.split(",")[1])





if __name__ == "__main__":
	print("[+] Stock Advice Bot Running")

	if not (os.path.exists("stock.db")):
		print("[-] No Database Detected")
		print("[+] Creating New Database")
		db.createDatabase()
	thread.start_new_thread(listen,())
	thread.start_new_thread(check,())
	thread.start_new_thread(que(),())
	try:
		print("<CTRL-C>")
		while True:
			pass
	except KeyboardInterrupt:
		print
		print("[-] Exiting")

