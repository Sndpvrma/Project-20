from django.shortcuts import render

from ORS.ctl.BaseCtl import BaseCtl
from ORS.utility.HtmlUtility import HtmlUtility
from service.models import Hotel
from service.service.HotelService import HotelService
from service.utility.DataValidator import DataValidator


class HotelCtl(BaseCtl):

    def preload(self, request):
        # Also make preload available under form for templates using `form.preload_data`
        self.form["preload_data"] = self.preload_data
        return self.preload_data

    # Populate Form from HTTP Request
    def request_to_form(self, request):
        self.form["id"] = request.get("id", 0)
        print('R2F =====================>', self.form["id"])
        self.form["hotel_id"] = request.get("hotelId", 0)
        self.form["hotel_name"] = request.get("hotelName", "")
        self.form["location"] = request.get("location", "")
        self.form["rating"] = request.get("rating", 0.0)
        self.form["contact_no"] = request.get("contactNo", "")

    # Populate Form from Model
    def model_to_form(self, obj):
        if obj == None:
            return
        self.form["id"] = obj.id
        # print('M2F======================>', self.form["id"])
        self.form["hotel_id"] = obj.hotel_id
        self.form["hotel_name"] = obj.hotel_name
        self.form["location"] = obj.location
        self.form["rating"] = obj.rating
        self.form["contact_no"] = obj.contact_no
        print('M2F======================>', self.form["contact_no"])


    # Convert form into module
    def form_to_model(self, obj):
        pk = int(self.form.get("id", 0))
        if pk > 0:
            obj.id = pk
        print('F2M======================>', obj.id)
        obj.hotel_id = int(self.form.get("hotel_id", 0))
        obj.hotel_name = self.form.get("hotel_name", "")
        obj.location = self.form.get("location", "")
        obj.rating = self.form.get("rating", 0.0)
        obj.contact_no = self.form.get("contact_no", "")
        return obj

    # Validate form
    def input_validation(self):
        super().input_validation()
        inputError = self.form["inputError"]
        if DataValidator.isNull(self.form["hotel_id"]):
            inputError["hotel_id"] = "Hotel Id is required"
            self.form["error"] = True
        if DataValidator.isNull(self.form["hotel_name"]):
            inputError["hotel_name"] = "Hotel Name is required"
            self.form["error"] = True
        if DataValidator.isNull(self.form["location"]):
            inputError["location"] = "Location is required"
            self.form["error"] = True
        if DataValidator.isNull(self.form["rating"]):
            inputError["rating"] = "Rating is required"
            self.form["error"] = True
        if DataValidator.isNull(self.form["contact_no"]):
            inputError["contact_no"] = "Contact No is required"
            self.form["error"] = True
        return self.form["error"]

    # Display Role page
    def display(self, request, params={}):
        if params["id"] > 0:
            hotel = self.get_service().get(params["id"])
            self.model_to_form(hotel)
        return render(
            request,
            self.get_template(),
            {"form": self.form, "preload_data": self.preload(request)},
        )

    # Submit Role page
    def submit(self, request, _params={}):
        hotel = self.form_to_model(Hotel())
        self    .get_service().save(hotel)
        if int(self.form["id"]) > 0:
            self.form["id"] = hotel.id
        self.form["error"] = False
        self.form["message"] = "Data is saved"
        return render(
            request,
            self.get_template(),
            {"form": self.form, "preload_data": self.preload(request)},
        )

    # Template html of Role page
    def get_template(self):
        return "ors/hotel.html"

    # Service of Role
    def get_service(self):
        return HotelService()
