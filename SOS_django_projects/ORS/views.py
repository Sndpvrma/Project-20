from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# Import controller classes
from ORS.ctl.UserCtl import UserCtl
from ORS.ctl.AccountCtl import AccountCtl
from ORS.ctl.CollegeCtl import CollegeCtl
from ORS.ctl.LoginCtl import LoginCtl
from ORS.ctl.LogoutCtl import LogoutCtl
from ORS.ctl.WelcomeCtl import WelcomeCtl
from ORS.ctl.RoleCtl import RoleCtl
from ORS.ctl.RoleListCtl import RoleListCtl
from ORS.ctl.FacultyCtl import FacultyCtl
from ORS.ctl.FacultyListCtl import FacultyListCtl
from ORS.ctl.CourseCtl import CourseCtl
from ORS.ctl.StudentCtl import StudentCtl
from ORS.ctl.MarksheetCtl import MarksheetCtl
from ORS.ctl.SubjectCtl import SubjectCtl
from ORS.ctl.SubjectListCtl import SubjectListCtl
from ORS.ctl.TimetableCtl import TimeTableCtl
from ORS.ctl.TimeTableListCtl import TimeTableListCtl
from ORS.ctl.UserListCtl import UserListCtl
from ORS.ctl.UserCtl import UserCtl
from ORS.ctl.CollegeListCtl import CollegeListCtl
from ORS.ctl.CourseListCtl import CourseListCtl
from ORS.ctl.MarksheetListCtl import MarksheetListCtl
from ORS.ctl.StudentListCtl import StudentListCtl
from ORS.ctl.RegistrationCtl import RegistrationCtl
from ORS.ctl.ForgetPasswordCtl import ForgetPasswordCtl
from ORS.ctl.ChangePasswordCtl import ChangePasswordCtl
from ORS.ctl.ProfileCtl import ProfileCtl
from ORS.ctl.parking_ctl import ParkingCtl
from ORS.ctl.parking_list_ctl import ParkingListCtl
from ORS.ctl.drone_ctl import DroneCtl
from ORS.ctl.drone_list_ctl import DroneListCtl
from ORS.ctl.weather_alert_ctl import WeatherAlertCtl
from ORS.ctl.weather_alert_list_ctl import WeatherAlertListCtl
from ORS.ctl.department_ctl import DepartmentCtl
from ORS.ctl.department_list_ctl import DepartmentListCtl
from ORS.ctl.Scholarship_ctl import ScholarshipCtl
from ORS.ctl.Scholarship_list_ctl import ScholarshipListCtl
from ORS.ctl.insurance_ctl import InsuranceCtl
from ORS.ctl.insurance_list_ctl import InsuranceListCtl
from ORS.ctl.Exam_ctl import ExamCtl
from ORS.ctl.Exam_list_ctl import ExamListCtl
from ORS.ctl.vendor_ctl import VendorCtl
from ORS.ctl.vendor_list_ctl import VendorListCtl
from ORS.ctl.library_ctl import LibraryCtl
from ORS.ctl.library_list_ctl import LibraryListCtl
from ORS.ctl.hotel_ctl import HotelCtl
from ORS.ctl.hotel_list_ctl import HotelListCtl
from ORS.ctl.payment_ctl import PaymentCtl
from ORS.ctl.payment_list_ctl import PaymentListCtl
from ORS.ctl.complaint_ctl import ComplaintCtl
from ORS.ctl.complaint_list_ctl import ComplaintListCtl

def info(request, page, action):
    """Log incoming request details (method, page, action, and path) to stdout."""
    print("REQ Method: ", request.method)
    print("Page: ", page)
    print("Action: ", action)
    print("File Path: ", __file__)
    print("Path: ", request.path)
    print("Full Path: ", request.get_full_path)


@csrf_exempt
def action_id(request, page, action="", id=0):
    """Route a request to the controller matching `page`, passing id=0."""
    print("------------------>1")
    info(request, page, action)
    ctlName = page + "Ctl()"
    ctlObj = eval(ctlName)
    return ctlObj.execute(request, {"id": id, "action": action})


@csrf_exempt
def action(request, page, action=""):
    """Route a request to the controller matching `page`, passing id=0."""
    print("------------------>1")
    info(request, page, action)
    ctlName = page + "Ctl()"
    ctlObj = eval(ctlName)
    return ctlObj.execute(request, {"id": 0, "action": action})


@csrf_exempt
def actionId(request, page, id=0):
    """Route a request to the controller matching `page`, passing the given `id`."""
    print("------------------>", id)
    info(request, page, id)
    ctlName = page + "Ctl()"
    ctlObj = eval(ctlName)
    return ctlObj.execute(request, {"id": id})


@csrf_exempt
def auth_action(request, page):
    """Route an authentication request (login, registration, etc.) to the matching controller."""
    print("Auth Action------------------>", page)
    info(request, page, 0)
    ctlName = page + "Ctl()"
    ctlObj = eval(ctlName)
    return ctlObj.execute(request, {})
