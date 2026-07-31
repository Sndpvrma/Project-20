from django.shortcuts import render

from ORS.ctl.BaseCtl import BaseCtl
from ORS.utility.HtmlUtility import HtmlUtility
from service.models import Exam
from service.service.ExamService import ExamService
from service.utility.DataValidator import DataValidator


class ExamCtl(BaseCtl):

    def preload(self, request):
        return self.preload_data

    # Populate Form from HTTP Request
    def request_to_form(self, request):
        self.form["id"] = request.get("id", 0)
        print('R2F =====================>', self.form["id"])
        self.form["exam_id"] = request.get("examId", 0)
        self.form["exam_name"] = request.get("examName", "")
        self.form["exam_date"] = request.get("examDate", "")
        self.form["total_marks"] = request.get("totalMarks", "")
        self.form["passing_marks"] = request.get("passingMarks", "")

    # Populate Form from Model
    def model_to_form(self, obj):
        if obj == None:
            return
        self.form["id"] = obj.id
        # print('M2F======================>', self.form["id"])
        self.form["exam_id"] = obj.exam_id
        self.form["exam_name"] = obj.exam_name
        self.form["exam_date"] = obj.exam_date
        self.form["total_marks"] = obj.total_marks
        self.form["passing_marks"] = obj.passing_marks
        print('M2F======================>', self.form["exam_date"])


    # Convert form into module
    def form_to_model(self, obj):
        pk = int(self.form.get("id", 0))
        if pk > 0:
            obj.id = pk
        print('F2M======================>', obj.id)
        obj.exam_id = int(self.form.get("exam_id", 0))
        obj.exam_name = self.form.get("exam_name", "")
        obj.exam_date = self.form.get("exam_date", "")
        obj.total_marks = self.form.get("total_marks", "")
        obj.passing_marks = self.form.get("passing_marks", "")
        return obj

    # Validate form
    def input_validation(self):
        super().input_validation()
        inputError = self.form["inputError"]
        if DataValidator.isNull(self.form["exam_id"]):
            inputError["exam_id"] = "Exam Id is required"
            self.form["error"] = True
        if DataValidator.isNull(self.form["exam_name"]):
            inputError["exam_name"] = "Exam Name is required"
            self.form["error"] = True
        if DataValidator.isNull(self.form["exam_date"]):
            inputError["exam_date"] = "Exam Date is required"
            self.form["error"] = True
        if DataValidator.isNull(self.form["total_marks"]):
            inputError["total_marks"] = "Total Marks is required"
            self.form["error"] = True
        if DataValidator.isNull(self.form["passing_marks"]):
            inputError["passing_marks"] = "Passing Marks is required"
            self.form["error"] = True
        return self.form["error"]

    # Display Role page
    def display(self, request, params={}):
        if params["id"] > 0:
            exam = self.get_service().get(params["id"])
            self.model_to_form(exam)
        return render(
            request,
            self.get_template(),
            {"form": self.form, "preload_data": self.preload(request)},
        )

    # Submit Role page
    def submit(self, request, _params={}):
        exam = self.form_to_model(Exam())
        self    .get_service().save(exam)
        if int(self.form["id"]) > 0:
            self.form["id"] = exam.id
        self.form["error"] = False
        self.form["message"] = "Data is saved"
        return render(
            request,
            self.get_template(),
            {"form": self.form, "preload_data": self.preload(request)},
        )

    # Template html of Role page
    def get_template(self):
        return "ors/exam.html"

    # Service of Role
    def get_service(self):
        return ExamService()
