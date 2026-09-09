from django.shortcuts import render

from ORS.ctl.BaseCtl import BaseCtl
from ORS.utility.HtmlUtility import HtmlUtility
from service.models import Vehicle
from service.service.VehicleService import VehicleService
from service.utility.DataValidator import DataValidator


class VehicleCtl(BaseCtl):

    def preload(self, request):
        self.form["preload_data"] = self.preload_data
        return self.preload_data

    def request_to_form(self, requestForm):
        self.form["id"] = requestForm.get("id", 0)
        self.form["vehicle_id"] = requestForm.get("vehicleId", 0)
        self.form["vehicle_name"] = requestForm.get("vehicleName", "")
        self.form["model"] = requestForm.get("model", "")
        self.form["color"] = requestForm.get("color", "")
        self.form["price"] = requestForm.get("price", 0.0)

    def model_to_form(self, obj):
        if obj == None:
            return
        self.form["id"] = obj.id
        self.form["vehicle_id"] = obj.vehicle_id
        self.form["vehicle_name"] = obj.vehicle_name
        self.form["model"] = obj.model
        self.form["color"] = obj.color
        self.form["price"] = obj.price

    def form_to_model(self, obj):
        pk = int(self.form.get("id", 0))
        if pk > 0:
            obj.id = pk
        obj.vehicle_id = int(self.form.get("vehicle_id", 0))
        obj.vehicle_name = self.form.get("vehicle_name", "")
        obj.model = self.form.get("model", "")
        obj.color = self.form.get("color", "")
        obj.price = self.form.get("price", 0.0)
        return obj

    def input_validation(self):
        super().input_validation()
        inputError = self.form["inputError"]

        if DataValidator.isNull(self.form["vehicle_id"]):
            inputError["vehicle_id"] = "Vehicle Id is required"
            self.form["error"] = True

        if DataValidator.isNull(self.form["vehicle_name"]):
            inputError["vehicle_name"] = "Vehicle Name is required"
            self.form["error"] = True

        if DataValidator.isNull(self.form["model"]):
            inputError["model"] = "Model is required"
            self.form["error"] = True

        if DataValidator.isNull(self.form["color"]):
            inputError["color"] = "Color is required"
            self.form["error"] = True

        if DataValidator.isNull(self.form["price"]):
            inputError["price"] = "Price is required"
            self.form["error"] = True

        return self.form["error"]

    def display(self, request, params={}):
        if params["id"] > 0:
            vehicle = self.get_service().get(params["id"])
            self.model_to_form(vehicle)

        res = render(
            request,
            self.get_template(),
            {"form": self.form, "preload_data": self.preload(request)},
        )
        return res

    def submit(self, request, params={}):
        vehicle = self.form_to_model(Vehicle())
        self.get_service().save(vehicle)

        self.form["id"] = vehicle.id
        self.form["error"] = False
        self.form["message"] = "Data is saved"

        res = render(
            request,
            self.get_template(),
            {"form": self.form, "preload_data": self.preload(request)},
        )
        return res

    def get_template(self):
        return "ors/vehicle.html"

    def get_service(self):
        return VehicleService()