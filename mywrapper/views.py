from django.shortcuts import render
import datetime
from django.utils import timezone
 # Create your views here.
# from mywrapper.models import Subject, SubjectComponents,Student,Teacher, SubjectsPerStudent,SubjectsPerTeacher, Attendance,DaysAttendanceWasTaken,Test,Marks
# from mywrapper.serializers import SubjectSerializer, StudentSerializer, AttendanceSerializer,SubjectsPerStudentSerializer,TestSerializer, MarksSerializer,DaysAttendanceWasTakenSerializer,TeacherSerializer,SubjectsPerTeacherSerializer,SubjectComponentsSerializer
from mywrapper.serializers import *

from rest_framework import generics
# from mywrapper.serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import authentication_classes
from rest_framework.decorators import permission_classes
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import permissions
from mywrapper.models import Profile

class IsTeacher(permissions.BasePermission):
	"""
	Global permission check for whether the user is a teacher
	"""

	def has_permission(self, request, view):
		if request.method in permissions.SAFE_METHODS:
			return True
		try:
			user = request.user
			profile = Profile.objects.get(user=user)
		except: 
			return False    
		if profile.is_teacher == True or profile.is_administrator == True:
			return True
		return False

class IsAdministrator(permissions.BasePermission):
	"""
	Global permission check for whether the user is a teacher
	"""

	def has_permission(self, request, view):
		if request.method in permissions.SAFE_METHODS:
			return True
		try:
			user = request.user
			profile = Profile.objects.get(user=user)
		except: 
			return False    
		if profile.is_administrator == True:
			return True
		return False

class SubjectList(generics.ListCreateAPIView):
	queryset = Subject.objects.all()
	serializer_class = SubjectSerializer

class SubjectDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = Subject.objects.all()
	serializer_class = SubjectSerializer

class SubjectComponentsList(generics.ListCreateAPIView):
	queryset = SubjectComponents.objects.all()
	serializer_class = SubjectComponentsSerializer

class SubjectComponentsDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = SubjectComponents.objects.all()
	serializer_class = SubjectComponentsSerializer

class SubjectsPerStudentList(generics.ListCreateAPIView):
	queryset = SubjectsPerStudent.objects.all()
	serializer_class = SubjectsPerStudentSerializer

class SubjectsPerStudentDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = SubjectsPerStudent.objects.all()
	serializer_class = SubjectsPerStudentSerializer

class SubjectsPerTeacherList(generics.ListCreateAPIView):
	queryset = SubjectsPerTeacher.objects.all()
	serializer_class = SubjectsPerTeacherSerializer

class SubjectsPerTeacherDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = SubjectsPerTeacher.objects.all()
	serializer_class = SubjectsPerTeacherSerializer

class StudentList(generics.ListCreateAPIView):
	queryset = Student.objects.all()
	serializer_class = StudentSerializer

class StudentDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = Student.objects.all()
	serializer_class = StudentSerializer

class TeacherList(generics.ListCreateAPIView):
	queryset = Teacher.objects.all()
	serializer_class = TeacherSerializer

class TeacherDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = Teacher.objects.all()
	serializer_class = TeacherSerializer

class AttendanceList(generics.ListCreateAPIView):
	queryset = Attendance.objects.all()
	serializer_class = AttendanceSerializer

class AttendanceDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = Attendance.objects.all()
	serializer_class = AttendanceSerializer

class TestList(generics.ListCreateAPIView):
	queryset = Test.objects.all()
	serializer_class = TestSerializer

class TestDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = Test.objects.all()
	serializer_class = TestSerializer

class MarksList(generics.ListCreateAPIView):
	queryset = Marks.objects.all()
	serializer_class = MarksSerializer

class MarksDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = Marks.objects.all()
	serializer_class = MarksSerializer

class DaysAttendanceWasTakenList(generics.ListCreateAPIView):
	queryset = DaysAttendanceWasTaken.objects.all()
	serializer_class = DaysAttendanceWasTakenSerializer

class DaysAttendanceWasTakenDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = DaysAttendanceWasTaken.objects.all()
	serializer_class = DaysAttendanceWasTakenSerializer

@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication,])
def getteachersubjects(request,pk):
	if request.method == 'GET':
		teacher = Teacher(id=pk)
		subjects = SubjectsPerTeacher.objects.filter(teacher=teacher)
		serializer = ReadSubjectsPerTeacherSerializer(subjects,many="True")
		return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication,])
def getstudentlistforcomponent(request,pk):
	if request.method == 'GET':
		subjectComponents = SubjectComponents(id=pk)
		students = SubjectsPerStudent.objects.filter(subjectComponents=subjectComponents)
		serializer = ReadSubjectsPerStudentSerializer(students,many="True") # Can use a cleaner serializer
		return Response(serializer.data)

@api_view(['GET','POST','PUT'])
@authentication_classes([JSONWebTokenAuthentication,])
# @permission_classes((IsTeacher, ))
def postabsentstudents(request):
	"""
	JSON Example
	{
	  "students": [1,2,3],
	  "teacher": 1,
	  "subjectcomponent": 2,
	  "date": "04/02/2016"
	}
	"""
	if request.method == 'POST':
		print request.data
		try:
			subjectComponents = SubjectComponents(pk=request.data['subjectcomponent'])
			date = datetime.datetime.strptime(request.data['date'], '%d/%m/%Y').strftime('%Y-%m-%d')
			daysAttendanceWasTaken = DaysAttendanceWasTaken(subjectComponents=subjectComponents, dateOfAttendance=date)
			daysAttendanceWasTaken.save()
		except:
			return Response({'id':-1, 'status': 'inaccurate input parameters'},status=status.HTTP_400_BAD_REQUEST)
		for studentid in request.data['students']:
			student = Student(pk=studentid)
			attendance = Attendance(student=student,dayAttendanceWasTaken=daysAttendanceWasTaken)
			attendance.save()
		return Response(status=status.HTTP_201_CREATED)
	# return Response(status=status.HTTP_400_BAD_REQUEST)

	if request.method == 'PUT':
		print request.data
		try:
			subjectComponents = SubjectComponents(pk=request.data['subjectcomponent'])
			date = datetime.datetime.strptime(request.data['date'], '%d/%m/%Y').strftime('%Y-%m-%d')
			daysAttendanceWasTaken = DaysAttendanceWasTaken.objects.get(subjectComponents=subjectComponents, dateOfAttendance=date)
		except:
			return Response({'id':-1, 'status': 'inaccurate input parameters'},status=status.HTTP_400_BAD_REQUEST)
		currentTime = timezone.now()
		elapsedTime =  currentTime - daysAttendanceWasTaken.timeAttendanceWasMarked
		if ((elapsedTime.total_seconds()/60) > 2 ):
			print "Too late!"
			return Response({'id':-1 ,'status': 'Too much time has changed since this data was entered'},status=status.HTTP_400_BAD_REQUEST)
			

		Attendance.objects.filter(dayAttendanceWasTaken=daysAttendanceWasTaken).delete()
		for studentid in request.data['students']:
			student = Student(pk=studentid)
			attendance = Attendance(student=student,dayAttendanceWasTaken=daysAttendanceWasTaken)
			attendance.save()
		return Response(status=status.HTTP_201_CREATED)
	return Response({'id':-1 ,'status': 'GET request not supported'},status=status.HTTP_400_BAD_REQUEST)

# class NoticeList(generics.ListCreateAPIView):
#     queryset = Notice.objects.all()
#     serializer_class = NoticeSerializer
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
#     def perform_create(self, serializer):
#     	serializer.save(owner=self.request.user)


# class NoticeDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Notice.objects.all()
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)a
#     serializer_class = NoticeSerializer

# class UserList(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

# class UserDetail(generics.RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer