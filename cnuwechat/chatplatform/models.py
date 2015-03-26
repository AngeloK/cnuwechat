# -*- coding: utf-8 -*-

from django.db import models

# Create your models here.

class Department(models.Model):

	'''
		Basic information for a department
		:departmentURL Home page url
	'''
	departmentName = models.CharField(max_length=50)
	departmentURL = models.URLField()

	class Meta:
		verbose_name = "Department"
		verbose_name_plural = "Departments"

	def __unicode__(self):
		return "%s Home Page:%s" %(self.departmentName,self.departmentURL)

class Student(models.Model):

	'''
		Basic information for a student
		:stuID ID in scholl card,
		:password: related to login offical scholl website
		:name true name
		:card_balance balance in school card based on the numbers show on teacing system "could incorrted sometime"
		:flow_balance balance for scholl network flow
	'''


	stuID = models.CharField(max_length=20,unique=True)
	password = models.CharField(max_length=100)
	name = models.CharField(max_length=100)
	departmentID = models.ForeignKey(Department)

	card_balance = models.CharField(max_length=100)
	flow_balance = models.CharField(max_length=100)

	class Meta:
		verbose_name = "Student"
		verbose_name_plural = "Students"

	def __unicode__(self):
		return "StudentID:%s,Name:%s" %(self.stuID,self.name)

                

class Teacher(models.Model):

	#Basic information for a teacher

	name = models.CharField(max_length=100)
	profession = models.CharField(max_length=100)


	class Meta:
		verbose_name = "teacher"
		verbose_name_plural = "teachers"

	def __unicode__(self):
		return "%s-%s" %(self.name,self.profession)
		

class Course(models.Model):

	'''
		Basic information for a course
		:courseName 
		:teacherID related to one teacher
	'''

	courseName = models.CharField(max_length=100)
	teacherID = models.ForeignKey(Teacher)

	class Meta:
		verbose_name = "course"
		verbose_name_plural = "courses"

	def __unicode__(self):
		return "%s-%s" %(self.courseName,self.teacherID)
	

class Schedule(models.Model):

	'''
		Course Schedule
	'''
	courseID = models.ForeignKey(Course)
	studentID = models.ForeignKey(Student,to_field='stuID')

	week = models.CharField(max_length=50)

	score = models.CharField(max_length=50,null=True)

	class Meta:
		verbose_name = "Schedule"
		verbose_name_plural = "Schedules"

	def __unicode__(self):
		return "StudentID:%s, CourseID:%s on %s" %(self.StudentID,self.courseID, \
																self.week)
	


