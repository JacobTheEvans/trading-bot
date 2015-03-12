import sqlite3 as db

def createDatabase():
	conn = db.connect("stock.db")
	cursor = conn.cursor()
	cursor.execute("create table stocks(name string,price string)")
	cursor.execute("create table que(name string, price string, time string)")
	conn.commit()
	conn.close()

def insertPrice(name,price):
	conn = db.connect("stock.db")
	cursor = conn.cursor()
	cursor.execute("insert into stocks values('%s','%s')" % (name,price))
	conn.commit()
	conn.close()

def loadPrices():
	conn = db.connect("stock.db")
	conn.row_factory = db.Row
	cursor = conn.cursor()
	cursor.execute("select * from stocks")
	rows = cursor.fetchall()
	data = []
	for row in rows:
		data.append(("%s,%s") % (row["name"],row["price"]))
	return data

def pastPrice(item):
	for i in loadPrices():
		if item in i:
			return float(i.split(",")[1])
	else:
		return False

def removePrice(iden):
	conn = db.connect("stock.db")
	cursor = conn.cursor()
	cursor.execute("delete from stocks where name='%s'" % iden)
	conn.commit()
	conn.close()

def insertQue(name,price,time):
	conn = db.connect("stock.db")
	cursor = conn.cursor()
	cursor.execute("insert into que values('%s','%s','%s')" % (name,price,time))
	conn.commit()
	conn.close()

def loadQue():
	conn = db.connect("stock.db")
	conn.row_factory = db.Row
	cursor = conn.cursor()
	cursor.execute("select * from que")
	rows = cursor.fetchall()
	data = []
	for row in rows:
		data.append(("%s,%s,%s") % (row["name"],row["price"],row["time"]))
	return data

def removeQue(iden):
	conn = db.connect("control.db")
	cursor = conn.cursor()
	cursor.execute("delete from que where name='%s'" % iden)
	conn.commit()
	conn.close()