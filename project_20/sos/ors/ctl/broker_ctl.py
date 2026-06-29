from .base_ctl import BaseCtl
from django.shortcuts import render
from service.models import Broker
from service.service.broker_service import BrokerService
from ..utility.data_validator import DataValidator


class BrokerCtl(BaseCtl):
    def request_to_form(self, request_form):
        self.form["id"] = request_form.get("id", 0)
        self.form["broker_name"] = request_form.get("broker_name", "").strip()
        self.form["contact_number"] = request_form.get("contact_number", "").strip()
        self.form["company"] = request_form.get("company", "").strip()

    def form_to_model(self, obj):
        obj.id = int(self.form.get("id", 0) or 0)
        obj.broker_name = self.form.get("broker_name", "").strip()
        obj.contact_number = self.form.get("contact_number", "").strip()
        obj.company = self.form.get("company", "").strip()
        return obj

    def model_to_form(self, obj):
        if obj == None:
            return
        self.form["id"] = obj.id
        self.form["broker_name"] = obj.broker_name
        self.form["contact_number"] = obj.contact_number
        self.form["company"] = obj.company

    def input_validation(self):
        super().input_validation()
        input_error = self.form["input_error"]

        if DataValidator.is_null(self.form["broker_name"]):
            input_error["broker_name"] = "Broker Name can not be null"  # Fixed message
            self.form["error"] = True
        if DataValidator.is_null(self.form["contact_number"]):
            input_error["contact_number"] = "Contact Number can not be null"  # Fixed message
            self.form["error"] = True
        elif not DataValidator.is_mobile_number(self.form.get("contact_number")):
            input_error["contact_number"] = "Contact Number must be 10 digits"
            self.form["error"] = True
        if DataValidator.is_null(self.form["company"]):
            input_error["company"] = "Company can not be null"  # Fixed message
            self.form["error"] = True

        return self.form["error"]

    def display(self, request, params={}):
        broker_id = int(params.get("id", 0))

        if broker_id > 0:
            broker = self.get_service().get(broker_id)
            self.model_to_form(broker)
        res = render(request, self.get_template(), {
            "form": self.form,
            "preload_data": self.preload(request)
        })
        return res

    def submit(self, request, params={}):

        duplicate = self.get_service().get_model().objects.filter(broker_name=self.form.get('broker_name', ''))

        if duplicate.exists():
            self.form['error'] = True
            self.form['message'] = "Broker already exist"
        else:
            broker = self.form_to_model(Broker())
            self.get_service().save(broker)
            self.form['id'] = broker.id
            self.form['error'] = False
            self.form['message'] = "Broker added successfully..!!"

        res = render(request, self.get_template(), {
            "form": self.form,
            "preload_data": self.preload(request)
        })
        return res

    def get_template(self):
        return "broker.html"

    def get_service(self):
        return BrokerService()