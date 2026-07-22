from django.shortcuts import render

from ORS.ctl.BaseCtl import BaseCtl
from ORS.utility.HtmlUtility import HtmlUtility
from service.models import Parking
from service.service.ParkingService import ParkingService
from service.utility.DataValidator import DataValidator


class ParkingCtl(BaseCtl):

    def preload(self, request):
        status_list = ["Occupied", "Available", "Reserved", "Complete"]
        print("Preload status:", repr(self.form.get("status")))
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
        self.form["parking_id"] = request.get("parkingId", 0)
        self.form["parking_code"] = request.get("parkingCode", "")
        self.form["vehicle_number"] = request.get("vehicleNumber", "")
        self.form["slot_number"] = request.get("slotNumber", "")
        self.form["status"] = request.get("status", "")

    # Populate Form from Model
    def model_to_form(self, obj):
        if obj == None:
            return
        self.form["id"] = obj.id
        # print('M2F======================>', self.form["id"])
        self.form["parking_id"] = obj.parking_id
        self.form["parking_code"] = obj.parking_code
        self.form["vehicle_number"] = obj.vehicle_number
        self.form["slot_number"] = obj.slot_number
        self.form["status"] = obj.status
        print('M2F======================>', self.form["status"])


    # Convert form into module
    def form_to_model(self, obj):
        pk = int(self.form.get("id", 0))
        if pk > 0:
            obj.id = pk
        print('F2M======================>', obj.id)
        obj.parking_id = int(self.form.get("parking_id", 0))
        obj.parking_code = self.form.get("parking_code", "")
        obj.vehicle_number = self.form.get("vehicle_number", "")
        obj.slot_number = self.form.get("slot_number", "")
        obj.status = self.form.get("status", "")
        return obj

    # Validate form
    def input_validation(self):
        super().input_validation()
        inputError = self.form["inputError"]
        if DataValidator.isNull(self.form["parking_id"]):
            inputError["parking_id"] = "Parking Id is required"
            self.form["error"] = True
        if DataValidator.isNull(self.form["parking_code"]):
            inputError["parking_code"] = "Parking Code is required"
            self.form["error"] = True
        if DataValidator.isNull(self.form["vehicle_number"]):
            inputError["vehicle_number"] = "Vehicle No is required"
            self.form["error"] = True
        if DataValidator.isNull(self.form["slot_number"]):
            inputError["slot_number"] = "Slot No is required"
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
        parking = self.form_to_model(Parking())
        self.get_service().save(parking)
        if int(self.form["id"]) > 0:
            self.form["id"] = parking.id
        self.form["error"] = False
        self.form["message"] = "Data is saved"
        return render(
            request,
            self.get_template(),
            {"form": self.form, "preload_data": self.preload(request)},
        )

    # Template html of Role page
    def get_template(self):
        return "ors/parking.html"

    # Service of Role
    def get_service(self):
        return ParkingService()
