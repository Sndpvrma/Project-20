from .base_ctl import BaseCtl
from django.shortcuts import render
from service.models import Patient
from service.service.patient_service import PatientService
from ..utility.data_validator import DataValidator

class PatientCtl(BaseCtl):
    def request_to_form(self, request_form):
        self.form["id"] = request_form.get("id", 0)
        self.form["patient_name"] = request_form.get("patient_name", "").strip()
        self.form["disease"] = request_form.get("disease", "").strip()
        self.form["doctor_name"] = request_form.get("doctor_name", "").strip()
        self.form["age"] = request_form.get("age", 0).strip()

    def form_to_model(self, obj):

        obj.id = 0

        obj.patient_name = self.form.get("patient_name", "")
        obj.disease = self.form.get("disease", "")
        obj.doctor_name = self.form.get("doctor_name", "")
        obj.age = self.form.get("age", 0)

        return obj

    def model_to_form(self, obj):
        if obj == None:
            return
        self.form["id"] = obj.id
        self.form["patient_name"] = obj.patient_name
        self.form["disease"] = obj.disease
        self.form["doctor_name"] = obj.doctor_name
        self.form["age"] = obj.age

    def input_validation(self):

        super().input_validation()

        input_error = self.form.get("input_error", {})

        if DataValidator.is_null(self.form.get("patient_name")):
            input_error["patient_name"] = "Patient Name can not be null"
            self.form["error"] = True

        if DataValidator.is_null(self.form.get("disease")):
            input_error["disease"] = "disease can not be null"
            self.form["error"] = True

        if DataValidator.is_null(self.form.get("doctor_name")):
            input_error["doctor_name"] = "Doctor Name can not be null"
            self.form["error"] = True

        if DataValidator.is_null(self.form.get("age")):
            input_error["age"] = "Age can not be null"
            self.form["error"] = True

        return self.form.get("error", False)

    def preload(self, request):
        pass

    def display(self, request, params={}):
        patient_id = int(params.get("id", 0))

        if patient_id > 0:
            patient = self.get_service().get(patient_id)
            self.model_to_form(patient)
        res = render(request, self.get_template(), {
            "form": self.form,
            "preload_data": self.preload(request)
        })
        return res

    # def submit(self, request, params={}):
    #
    #     duplicate = self.get_service().get_model().objects.filter(patient_name=self.form.get('patient_name', ''))
    #
    #     if duplicate.exists():
    #         self.form['error'] = True
    #         self.form['message'] = "Patient ID already exist"
    #     else:
    #         user = self.form_to_model(Patient())
    #         self.get_service().save(user)
    #
    #         self.form['id'] = user.id
    #         self.form['error'] = False
    #         self.form['message'] = "Patient added successfully..!!"
    #
    #     res = render(request, self.get_template(), {
    #         "form": self.form,
    #         "preload_data": self.preload(request)
    #     })
    #     return res

    def submit(self, request, params={}):

        pk = int(self.form.get('id', 0))

        duplicate = self.get_service().get_model().objects.filter(patient_name=self.form.get('patient_name', ''))

        if pk > 0:
            duplicate = duplicate.exclude(id=pk)

        if duplicate.exists():
            self.form['error'] = True
            self.form['message'] = "Patient ID already exist"
        else:
            if pk > 0:
                patient_obj = self.get_service().get_model().objects.get(id=pk)
                patient = self.form_to_model(patient_obj)
                patient.id = pk
            else:
                patient = self.form_to_model(Patient())

            self.get_service().save(patient)

            self.form['id'] = str(patient.id)
            self.form['error'] = False

            if pk > 0:
                self.form['message'] = "Patient updated successfully..!!"
            else:
                self.form['message'] = "Patient added successfully..!!"

        res = render(request, self.get_template(), {
            "form": self.form,
            "preload_data": self.preload(request)
        })
        return res

    def get_template(self):
        return "patient.html"

    def get_service(self):
        return PatientService()
