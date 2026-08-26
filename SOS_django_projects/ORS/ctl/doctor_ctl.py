from django.shortcuts import render

from ORS.ctl.BaseCtl import BaseCtl
from ORS.utility.HtmlUtility import HtmlUtility
from service.models import Doctor
from service.service.DoctorService import DoctorService
from service.utility.DataValidator import DataValidator


class DoctorCtl(BaseCtl):

    def preload(self, request):
        # Also make preload available under form for templates using `form.preload_data`
        self.form["preload_data"] = self.preload_data
        return self.preload_data

    # Populate Form from HTTP Request
    def request_to_form(self, request):
        self.form["id"] = request.get("id", 0)
        print('R2F =====================>', self.form["id"])
        self.form["doctor_id"] = request.get("doctorId", 0)
        self.form["doctor_name"] = request.get("doctorName", "")
        self.form["specialization"] = request.get("specialization", "")
        self.form["experience"] = request.get("experience", 0)
        self.form["contact_no"] = request.get("contactNo", "")

    # Populate Form from Model
    def model_to_form(self, obj):
        if obj == None:
            return
        self.form["id"] = obj.id
        # print('M2F======================>', self.form["id"])
        self.form["doctor_id"] = obj.doctor_id
        self.form["doctor_name"] = obj.doctor_name
        self.form["specialization"] = obj.specialization
        self.form["experience"] = obj.experience
        self.form["contact_no"] = obj.contact_no
        print('M2F======================>', self.form["contact_no"])


    # Convert form into module
    def form_to_model(self, obj):
        pk = int(self.form.get("id", 0))
        if pk > 0:
            obj.id = pk
        print('F2M======================>', obj.id)
        obj.doctor_id = int(self.form.get("doctor_id", 0))
        obj.doctor_name = self.form.get("doctor_name", "")
        obj.specialization = self.form.get("specialization", "")
        obj.experience = self.form.get("experience", "")
        obj.contact_no = self.form.get("contact_no", "")
        return obj

    # Validate form
    def input_validation(self):
        super().input_validation()
        inputError = self.form["inputError"]
        if DataValidator.isNull(self.form["doctor_id"]):
            inputError["doctor_id"] = "Doctor Id is required"
            self.form["error"] = True
        if DataValidator.isNull(self.form["doctor_name"]):
            inputError["doctor_name"] = "Doctor Name is required"
            self.form["error"] = True
        if DataValidator.isNull(self.form["specialization"]):
            inputError["specialization"] = "Specialization is required"
            self.form["error"] = True
        if DataValidator.isNull(self.form["experience"]):
            inputError["experience"] = "Experience is required"
            self.form["error"] = True
        if DataValidator.isNull(self.form["contact_no"]):
            inputError["contact_no"] = "Contact No is required"
            self.form["error"] = True
        return self.form["error"]

    # Display Role page
    def display(self, request, params={}):
        if params["id"] > 0:
            doctor = self.get_service().get(params["id"])
            self.model_to_form(doctor)
        return render(
            request,
            self.get_template(),
            {"form": self.form, "preload_data": self.preload(request)},
        )

    # Submit Role page
    def submit(self, request, _params={}):
        doctor = self.form_to_model(Doctor())
        self    .get_service().save(doctor)
        if int(self.form["id"]) > 0:
            self.form["id"] = doctor.id
        self.form["error"] = False
        self.form["message"] = "Data is saved"
        return render(
            request,
            self.get_template(),
            {"form": self.form, "preload_data": self.preload(request)},
        )

    # Template html of Role page
    def get_template(self):
        return "ors/doctor.html"

    # Service of Role
    def get_service(self):
        return DoctorService()
