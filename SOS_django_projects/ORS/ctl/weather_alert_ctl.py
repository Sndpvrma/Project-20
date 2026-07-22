from django.shortcuts import render

from ORS.ctl.BaseCtl import BaseCtl
from ORS.utility.HtmlUtility import HtmlUtility
from service.models import WeatherAlert
from service.service.WeatherAlertService import WeatherAlertService
from service.utility.DataValidator import DataValidator




class WeatherAlertCtl(BaseCtl):

    def preload(self, request):
        status_list = [
            "Normal",
            "Heat Wave",
            "Heavy Rain",
            "Thunderstorm",
            "Flood Warning",
            "Cold Wave"
        ]
        # print("Preload status:", repr(self.form.get("status")))
        self.preload_data["status_select"] = HtmlUtility.get_list_from_list(
            "status",
            self.form.get("status"),
            status_list,
        )
        # Also make preload available under form for templates using `form.preload_data`
        self.form["preload_data"] = self.preload_data
        return self.preload_data

    # Populate Form from HTTP Request
    def request_to_form(self, request):
        self.form["id"] = request.get("id", 0)
        print('R2F =====================>', self.form["id"])
        self.form["alert_id"] = request.get("alertId", 0)
        self.form["alert_code"] = request.get("alertCode", "")
        self.form["city_name"] = request.get("cityName", "")
        self.form["temperature"] = request.get("temperature", "")
        self.form["status"] = request.get("status", "")

    # Populate Form from Model
    def model_to_form(self, obj):
        if obj == None:
            return
        self.form["id"] = obj.id
        # print('M2F======================>', self.form["id"])
        self.form["alert_id"] = obj.alert_id
        self.form["alert_code"] = obj.alert_code
        self.form["city_name"] = obj.city_name
        self.form["temperature"] = obj.temperature
        self.form["status"] = obj.status
        print('M2F======================>', self.form["status"])


    # Convert form into module
    def form_to_model(self, obj):
        pk = int(self.form.get("id", 0))
        if pk > 0:
            obj.id = pk
        print('F2M======================>', obj.id)
        obj.alert_id = int(self.form.get("alert_id", 0))
        obj.alert_code = self.form.get("alert_code", "")
        obj.city_name = self.form.get("city_name", "")
        obj.temperature = self.form.get("temperature", "")
        obj.status = self.form.get("status", "")
        return obj

    # Validate form
    def input_validation(self):
        super().input_validation()
        inputError = self.form["inputError"]
        if DataValidator.isNull(self.form["alert_id"]):
            inputError["alert_id"] = "Alert Id is required"
            self.form["error"] = True
        if DataValidator.isNull(self.form["alert_code"]):
            inputError["alert_code"] = "Alert Code is required"
            self.form["error"] = True
        if DataValidator.isNull(self.form["city_name"]):
            inputError["city_name"] = "City Name is required"
            self.form["error"] = True
        if DataValidator.isNull(self.form["temperature"]):
            inputError["temperature"] = "Temperature is required"
            self.form["error"] = True
        if DataValidator.isNull(self.form["status"]):
            inputError["status"] = "Status is required"
            self.form["error"] = True
        return self.form["error"]

    # Display Role page
    def display(self, request, params={}):
        if params["id"] > 0:
            alert = self.get_service().get(params["id"])
            self.model_to_form(alert)
        return render(
            request,
            self.get_template(),
            {"form": self.form, "preload_data": self.preload(request)},
        )

    # Submit Role page
    def submit(self, request, _params={}):
        alert = self.form_to_model(WeatherAlert())
        self    .get_service().save(alert)
        if int(self.form["id"]) > 0:
            self.form["id"] = alert.id
        self.form["error"] = False
        self.form["message"] = "Data is saved"
        return render(
            request,
            self.get_template(),
            {"form": self.form, "preload_data": self.preload(request)},
        )

    # Template html of Role page
    def get_template(self):
        return "ors/weatheralert.html"

    # Service of Role
    def get_service(self):
        return WeatherAlertService()
