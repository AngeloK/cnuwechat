# -*- coding: utf-8 -*-

import MySQLdb
import random


def addOnePerson(num):
	db = MySQLdb.connect('localhost','root','','cnuwechat')
	c = db.cursor()

	id_tail = ''
	password = '123456'

	for i in range(1,num+1):
		if i < 10:
			id_tail = '00'+str(i)
		elif i>=10 and i<100:
			id_tail = '0'+str(i)
		else:
			id_tail = str(i)

		studentID = '1110500'+id_tail
		name = 'Test{'+str(i)+'}'
		departmentID = random.randint(1,7)
		card_balance = str(random.uniform(0,100))
		flow_balance = str(random.uniform(0,100))

		sql_com = "INSERT INTO `cnuwechat`.`chatplatform_student` (`stuID`,`password`,`name`,`card_balance`,\
`flow_balance`,`departmentID_id`) \
VALUES ('%s','%s','%s','%s','%s','%s');" %(studentID,password,name, \
card_balance,flow_balance,departmentID)
		c.execute(sql_com)
	db.commit()
	c.close()
	db.close()
	print '-'*20
	print "Person data added successfully!"


def addDepartment(num):
	pass



def addTeacher(num):
	db = MySQLdb.connect('localhost','root','','cnuwechat')
	c = db.cursor()

	professions = ['Mathematics','Computer Science','Chinese','Biology','Chemistry','History',"Physics"]

	for i in range(1,num+1):
		teacherName = 'Teacher'+str(i)
		profession = random.choice(professions)

		sql_com = "INSERT INTO `cnuwechat`.`chatplatform_teacher` (`name`,`profession`) VALUES ('%s','%s');" \
%(teacherName,profession)
	
		c.execute(sql_com)

	db.commit()
	c.close()
	db.close()
	print '-'*20
	print "Teachers data added successfully!"

def addCourse(num):
	db = MySQLdb.connect('localhost','root','','cnuwechat')
	c = db.cursor()

	for i in range(1,num+1):
		courseName = 'course'+str(i)
		teacherID = random.choice(range(2,21))

		sql_com = "INSERT INTO `cnuwechat`.`chatplatform_course`(`courseName`,`teacherID_id`) VALUES \
('%s','%s');" %(courseName,teacherID)
		c.execute(sql_com)


	db.commit()
	c.close()
	db.close()
	print '-'*20
	print "Courses data added successfully!"

def addSechdule(num):
	db = MySQLdb.connect('localhost','root','','cnuwechat')
	c = db.cursor()	

	sel_stuid_sql = "SELECT stuID from `cnuwechat`.`chatplatform_student`;"
	c.execute(sel_stuid_sql)
	stuid_results = c.fetchall()
	stu_list = [stuID for stuID in [item[0] for item in stuid_results]]

	sel_courseid_sql = "SELECT id from `cnuwechat`.`chatplatform_course`;"
	c.execute(sel_courseid_sql)
	courseid_results = c.fetchall()
	course_list = [courseid for courseid in [item[0] for item in courseid_results]]

	for i in range(1,num+1):
		studentID = random.choice(stu_list)
		courseID = random.choice(course_list)
		week = random.choice(range(1,8))
		score = random.choice([random.randint(1,100),''])

		sql_com = "INSERT INTO `cnuwechat`.`chatplatform_schedule` (`week`,`score`,`courseID_id`,`studentID_id`) \
VALUES ('%s','%s','%s','%s');" %(week,score,courseID,studentID)
		c.execute(sql_com)


	db.commit()
	c.close()
	db.close()
	print '-'*20
	print "schedule data added successfully!"


if __name__ == '__main__':
	# addOnePerson(100)
	# addTeacher(20)
	# addCourse(20)
	# addSechdule(50)

