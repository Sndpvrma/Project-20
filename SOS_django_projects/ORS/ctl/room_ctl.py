from django.shortcuts import render

from ORS.ctl.BaseCtl import BaseCtl
from ORS.utility.HtmlUtility import HtmlUtility
from service.models import Room
from service.service.RoomService import RoomService
from service.utility.DataValidator import DataValidator


class RoomCtl(BaseCtl):

    def preload(self, request):
        self.form["preload_data"] = self.preload_data
        return self.preload_data

    def request_to_form(self, requestForm):
        self.form["id"] = requestForm.get("id", 0)
        self.form["room_id"] = requestForm.get("roomId", 0)
        self.form["room_number"] = requestForm.get("roomNumber", "")
        self.form["room_type"] = requestForm.get("roomType", "")
        self.form["price_per_day"] = requestForm.get("pricePerDay", 0.0)
        self.form["availability"] = requestForm.get("availability", "")
        

    def model_to_form(self, obj):
        if obj == None:
            return
        self.form["id"] = obj.id
        self.form["room_id"] = obj.room_id
        self.form["room_number"] = obj.room_number
        self.form["room_type"] = obj.room_type
        self.form["price_per_day"] = obj.price_per_day
        self.form["availability"] = obj.availability


    def form_to_model(self, obj):
        pk = int(self.form.get("id", 0))
        if pk > 0:
            obj.id = pk
        obj.room_id = int(self.form.get("room_id", 0))
        obj.room_number = self.form.get("room_number", "")
        obj.room_type = self.form.get("room_type", "")
        obj.price_per_day = self.form.get("price_per_day", 0.0)
        obj.availability = self.form.get("availability", "")
        return obj

    def input_validation(self):
        super().input_validation()
        inputError = self.form["inputError"]

        if DataValidator.isNull(self.form["room_id"]):
            inputError["room_id"] = "Room Id is required"
            self.form["error"] = True

        if DataValidator.isNull(self.form["room_number"]):
            inputError["room_number"] = "Room Number is required"
            self.form["error"] = True

        if DataValidator.isNull(self.form["room_type"]):
            inputError["room_type"] = "Room Type is required"
            self.form["error"] = True

        if DataValidator.isNull(self.form["price_per_day"]):
            inputError["price_per_day"] = "Price Per Day is required"
            self.form["error"] = True

        if DataValidator.isNull(self.form["availability"]):
            inputError["availability"] = "Availability is required"
            self.form["error"] = True

        return self.form["error"]

    def display(self, request, params={}):
        if params["id"] > 0:
            room = self.get_service().get(params["id"])
            self.model_to_form(room)

        res = render(
            request,
            self.get_template(),
            {"form": self.form, "preload_data": self.preload(request)},
        )
        return res

    def submit(self, request, params={}):
        room = self.form_to_model(Room())
        self.get_service().save(room)

        self.form["id"] = room.id
        self.form["error"] = False
        self.form["message"] = "Data is saved"

        res = render(
            request,
            self.get_template(),
            {"form": self.form, "preload_data": self.preload(request)},
        )
        return res

    def get_template(self):
        return "ors/room.html"

    def get_service(self):
        return RoomService()