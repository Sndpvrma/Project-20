from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

# Import controller classes
from .ctl.welcome_ctl import WelcomeCtl
from .ctl.role_ctl import RoleCtl
from .ctl.role_list_ctl import RoleListCtl
from .ctl.registration_ctl import RegistrationCtl
from .ctl.login_ctl import LoginCtl
from .ctl.user_ctl import UserCtl
from .ctl.user_list_ctl import UserListCtl
from .ctl.college_ctl import CollegeCtl
from .ctl.college_list_ctl import CollegeListCtl
from .ctl.course_ctl import CourseCtl
from .ctl.course_list_ctl import CourseListCtl
from .ctl.marksheet_ctl import MarksheetCtl
from .ctl.marksheet_list_ctl import MarksheetListCtl
from .ctl.student_ctl import StudentCtl
from .ctl.student_list_ctl import StudentListCtl
from .ctl.subject_ctl import SubjectCtl
from .ctl.subject_list_ctl import SubjectListCtl
from .ctl.time_table_ctl import TimeTableCtl
from .ctl.time_table_list_ctl import TimeTableListCtl
from .ctl.faculty_ctl import FacultyCtl
from .ctl.faculty_list_ctl import FacultyListCtl
from .ctl.patient_ctl import PatientCtl
from .ctl.patient_list_ctl import PatientListCtl
from .ctl.broker_ctl import BrokerCtl
from .ctl.broker_list_ctl import BrokerListCtl
from .ctl.employee_ctl import EmployeeCtl
from .ctl.employee_list_ctl import EmployeeListCtl
from .ctl.logout_ctl import LogoutCtl
from .ctl.forget_password_ctl import ForgetPasswordCtl
from .ctl.change_password_ctl import ChangePasswordCtl

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
    print(ctlName)
    return ctlObj.execute(request, {"id": 0, "action": action})


@csrf_exempt
def actionId(request, page, id=0):
    """Route a request to the controller matching `page`, passing the given `id`."""
    print("------------------>", id)
    info(request, page, id)
    ctlName = page + "Ctl()" # "WelcomeCtl()"
    ctlObj = eval(ctlName) # WelcomeCtl()
    return ctlObj.execute(request, {"id": id})


@csrf_exempt
def auth_action(request, page):
    """Route an authentication request (login, registration, etc.) to the matching controller."""
    print("Auth Action------------------>", page)
    info(request, page, 0)
    ctlName = page + "Ctl()"
    ctlObj = eval(ctlName)
    return ctlObj.execute(request, {})


@csrf_exempt
def preload_router(request, page):
    print('ppppppppppppppppppppppppppppppppppp', page)
    info(request, page, 0)
    ctlName = page + "Ctl()"
    ctlObj = eval(ctlName)
    data = ctlObj.preload(request)
    return JsonResponse(data)

