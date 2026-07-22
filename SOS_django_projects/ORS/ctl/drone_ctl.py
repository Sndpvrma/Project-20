from django.shortcuts import render

from ORS.ctl.BaseCtl import BaseCtl
from ORS.utility.HtmlUtility import HtmlUtility
from service.models import Drone
from service.service.DroneService import DroneService
from service.utility.DataValidator import DataValidator


class DroneCtl(BaseCtl):

    def preload(self, request):
        status_list = [ "Available", "In Transit", "Charging", "Maintenance", "Offline"]
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
        self.form["drone_id"] = request.get("droneId", 0)
        self.form["drone_code"] = request.get("droneCode", "")
        self.form["operator_name"] = request.get("operatorName", "")
        self.form["delivery_zone"] = request.get("deliveryZone", "")
        self.form["status"] = request.get("status", "")

    # Populate Form from Model
    def model_to_form(self, obj):
        if obj == None:
            return
        self.form["id"] = obj.id
        # print('M2F======================>', self.form["id"])
        self.form["drone_id"] = obj.drone_id
        self.form["drone_code"] = obj.drone_code
        self.form["operator_name"] = obj.operator_name
        self.form["delivery_zone"] = obj.delivery_zone
        self.form["status"] = obj.status
        print('M2F======================>', self.form["status"])


    # Convert form into module
    def form_to_model(self, obj):
        pk = int(self.form.get("id", 0))
        if pk > 0:
            obj.id = pk
        print('F2M======================>', obj.id)
        obj.drone_id = int(self.form.get("drone_id", 0))
        obj.drone_code = self.form.get("drone_code", "")
        obj.operator_name = self.form.get("operator_name", "")
        obj.delivery_zone = self.form.get("delivery_zone", "")
        obj.status = self.form.get("status", "")
        return obj

    # Validate form
    def input_validation(self):
        super().input_validation()
        inputError = self.form["inputError"]
        if DataValidator.isNull(self.form["drone_id"]):
            inputError["drone_id"] = "Drone Id is required"
            self.form["error"] = True
        if DataValidator.isNull(self.form["drone_code"]):
            inputError["drone_code"] = "Drone Code is required"
            self.form["error"] = True
        if DataValidator.isNull(self.form["operator_name"]):
            inputError["operator_name"] = "Operator Name is required"
            self.form["error"] = True
        if DataValidator.isNull(self.form["delivery_zone"]):
            inputError["delivery_zone"] = "Delivery Zone is required"
            self.form["error"] = True
        if DataValidator.isNull(self.form["status"]):
            inputError["status"] = "Status is required"
            self.form["error"] = True
        return self.form["error"]

    # Display Role page
    def display(self, request, params={}):
        if params["id"] > 0:
            parking = self.get_service().get(params["id"])
            self.model_to_form(parking)
        return render(
            request,
            self.get_template(),
            {"form": self.form, "preload_data": self.preload(request)},
        )

    # Submit Role page
    def submit(self, request, _params={}):
        drone = self.form_to_model(Drone())
        self    .get_service().save(drone)
        if int(self.form["id"]) > 0:
            self.form["id"] = drone.id
        self.form["error"] = False
        self.form["message"] = "Data is saved"
        return render(
            request,
            self.get_template(),
            {"form": self.form, "preload_data": self.preload(request)},
        )

    # Template html of Role page
    def get_template(self):
        return "ors/drone.html"

    # Service of Role
    def get_service(self):
        return DroneService()
