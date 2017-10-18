import sqlite3

data = "peepscourses.db"

db = sqlite3.connect(data)
c = db.cursor()

avgs = {}

#compute each student's average
def findavg(nums):
	total = 0
	vals = 0
	for val in nums:
		total += val
		vals +=1
	return (1.0 * total)/vals

def createavgs():
#look up each students grades and add to the dictionary of averages
	find_grades = c.execute('SELECT peeps.id, mark FROM peeps, courses WHERE peeps.id = courses.id;')
	for row in find_grades:
		#print row
		if (avgs.has_key(row[0])):
			avgs[row[0]].append(row[1])
		else:
			avgs[row[0]] = [row[1]]
	#print avgs
	#value of key becomes average of grades
	for key in avgs:
		avgs[key] = findavg(avgs[key])

#display each student's name, id, and average
def display():
	for key in avgs:
		names = c.execute("SELECT name FROM peeps WHERE id = "+str(key)+";")
		for name in names:
			print name[0]+": "
		print "id="+str(key)+", "+"GPA="+str(avgs[key])

#Create a table of IDs and associated averages, named "peeps_avg"
def createtable():
	table = "CREATE TABLE peeps_avg (id INTEGER, avg DECIMAL);"
	c.execute(table)
	#insert values into table
	for key in avgs:
		c.execute("INSERT INTO peeps_avg VALUES ('%d', %d)" %(key, avgs[key])+";")

#Facilitate updating a student's average

#UPDATE
#change a record
#UPDATE <table> SET <field> = <value> WHERE <condition>;

# def updateavg(studentid, newavg):
# 	updatedtable = "UPDATE peeps_avg SET avg="+str(newavg)+"WHERE id =" +str(studentid)+";")
# 	c.execute(updatedtable)

def updateavg(studentid, newavg):
	updatedtable = "UPDATE peeps_avg SET avg =" + str(newavg) + " WHERE id =" + str(studentid) + ";"
	c.execute(updatedtable)

#Facilitate adding rows to the courses tables
def addcourse(ncode, nmark, nid):
	added = "INSERT INTO courses VALUES ('%s',%d,%d)" %(ncode, nmark, nid)+";"
	c.execute(added)

createavgs();
display();
createtable();
updateavg(3, 66)
addcourse("3darts", 99, 9)

db.commit()
db.close()