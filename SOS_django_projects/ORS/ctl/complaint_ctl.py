from django.shortcuts import render

from ORS.ctl.BaseCtl import BaseCtl
from ORS.utility.HtmlUtility import HtmlUtility
from service.models import Complaint
from service.service.ComplaintService import ComplaintService
from service.utility.DataValidator import DataValidator


class ComplaintCtl(BaseCtl):

    def preload(self, request):
        # Also make preload available under form for templates using `form.preload_data`
        self.form["preload_data"] = self.preload_data
        return self.preload_data

    # Populate Form from HTTP Request
    def request_to_form(self, request):
        self.form["id"] = request.get("id", 0)
        print('R2F =====================>', self.form["id"])
        self.form["complaint_id"] = request.get("complaintId", 0)
        self.form["complaint_type"] = request.get("complaintType", "")
        self.form["description"] = request.get("description", "")
        self.form["complaint_date"] = request.get("complaintDate", "")
        self.form["status"] = request.get("status", "")

    # Populate Form from Model
    def model_to_form(self, obj):
        if obj == None:
            return
        self.form["id"] = obj.id
        # print('M2F======================>', self.form["id"])
        self.form["complaint_id"] = obj.complaint_id
        self.form["complaint_type"] = obj.complaint_type
        self.form["description"] = obj.description
        self.form["complaint_date"] = obj.complaint_date
        self.form["status"] = obj.status
        print('M2F======================>', self.form["status"])


    # Convert form into module
    def form_to_model(self, obj):
        pk = int(self.form.get("id", 0))
        if pk > 0:
            obj.id = pk
        print('F2M======================>', obj.id)
        obj.complaint_id = int(self.form.get("complaint_id", 0))
        obj.complaint_type = self.form.get("complaint_type", "")
        obj.description = self.form.get("description", "")
        obj.complaint_date = self.form.get("complaint_date", "")
        obj.status = self.form.get("status", "")
        return obj

    # Validate form
    def input_validation(self):
        super().input_validation()
        inputError = self.form["inputError"]
        if DataValidator.isNull(self.form["complaint_id"]):
            inputError["complaint_id"] = "Complaint Id is required"
            self.form["error"] = True
        if DataValidator.isNull(self.form["complaint_type"]):
            inputError["complaint_type"] = "Complaint Type is required"
            self.form["error"] = True
        if DataValidator.isNull(self.form["description"]):
            inputError["description"] = "Description is required"
            self.form["error"] = True
        if DataValidator.isNull(self.form["complaint_date"]):
            inputError["complaint_date"] = "Complaint Date is required"
            self.form["error"] = True
        if DataValidator.isNull(self.form["status"]):
            inputError["status"] = "Status is required"
            self.form["error"] = True
        return self.form["error"]

    # Display Role page
    def display(self, request, params={}):
        if params["id"] > 0:
            complaint = self.get_service().get(params["id"])
            self.model_to_form(complaint)
        return render(
            request,
            self.get_template(),
            {"form": self.form, "preload_data": self.preload(request)},
        )

    # Submit Role page
    def submit(self, request, _params={}):
        complaint = self.form_to_model(Complaint())
        self    .get_service().save(complaint)
        if int(self.form["id"]) > 0:
            self.form["id"] = complaint.id
        self.form["error"] = False
        self.form["message"] = "Data is saved"
        return render(
            request,
            self.get_template(),
            {"form": self.form, "preload_data": self.preload(request)},
        )

    # Template html of Role page
    def get_template(self):
        return "ors/complaint.html"

    # Service of Role
    def get_service(self):
        return ComplaintService()
