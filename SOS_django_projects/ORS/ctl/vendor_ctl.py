from django.shortcuts import render

from ORS.ctl.BaseCtl import BaseCtl
from ORS.utility.HtmlUtility import HtmlUtility
from service.models import Vendor
from service.service.VendorService import VendorService
from service.utility.DataValidator import DataValidator


class VendorCtl(BaseCtl):

    def preload(self, request):
        service_type_list = [
            "Maintenance",
            "Repairing",
            "Logistics"
        ]
        # print("Preload service_type:", repr(self.form.get("service_type")))
        self.preload_data["service_type_select"] = HtmlUtility.get_list_from_list(
            "service_type",
            self.form.get("service_type"),
            service_type_list,
        )
        # Also make preload available under form for templates using `form.preload_data`
        self.form["preload_data"] = self.preload_data
        return self.preload_data

    # Populate Form from HTTP Request
    def request_to_form(self, request):
        self.form["id"] = request.get("id", 0)
        print('R2F =====================>', self.form["id"])
        self.form["vendor_id"] = request.get("vendorId", 0)
        self.form["vendor_name"] = request.get("vendorName", "")
        self.form["mobile_no"] = request.get("mobileNo", "")
        self.form["address"] = request.get("address", "")
        self.form["service_type"] = request.get("service_type", "")

    # Populate Form from Model
    def model_to_form(self, obj):
        if obj == None:
            return
        self.form["id"] = obj.id
        # print('M2F======================>', self.form["id"])
        self.form["vendor_id"] = obj.vendor_id
        self.form["vendor_name"] = obj.vendor_name
        self.form["mobile_no"] = obj.mobile_no
        self.form["address"] = obj.address
        self.form["service_type"] = obj.service_type
        print('M2F======================>', self.form["service_type"])


    # Convert form into module
    def form_to_model(self, obj):
        pk = int(self.form.get("id", 0))
        if pk > 0:
            obj.id = pk
        print('F2M======================>', obj.id)
        obj.vendor_id = int(self.form.get("vendor_id", 0))
        obj.vendor_name = self.form.get("vendor_name", "")
        obj.mobile_no = self.form.get("mobile_no", "")
        obj.address = self.form.get("address", "")
        obj.service_type = self.form.get("service_type", "")
        return obj

    # Validate form
    def input_validation(self):
        super().input_validation()
        inputError = self.form["inputError"]
        if DataValidator.isNull(self.form["vendor_id"]):
            inputError["vendor_id"] = "Vendor Id is required"
            self.form["error"] = True
        if DataValidator.isNull(self.form["vendor_name"]):
            inputError["vendor_name"] = "Vendor Name is required"
            self.form["error"] = True
        if DataValidator.isNull(self.form["mobile_no"]):
            inputError["mobile_no"] = "Mobile No is required"
            self.form["error"] = True
        if DataValidator.isNull(self.form["address"]):
            inputError["address"] = "Address is required"
            self.form["error"] = True
        if DataValidator.isNull(self.form["service_type"]):
            inputError["service_type"] = "Service Type is required"
            self.form["error"] = True
        return self.form["error"]

    # Display Role page
    def display(self, request, params={}):
        if params["id"] > 0:
            vendor = self.get_service().get(params["id"])
            self.model_to_form(vendor)
        return render(
            request,
            self.get_template(),
            {"form": self.form, "preload_data": self.preload(request)},
        )

    # Submit Role page
    def submit(self, request, _params={}):
        vendor = self.form_to_model(Vendor())
        self    .get_service().save(vendor)
        if int(self.form["id"]) > 0:
            self.form["id"] = vendor.id
        self.form["error"] = False
        self.form["message"] = "Data is saved"
        return render(
            request,
            self.get_template(),
            {"form": self.form, "preload_data": self.preload(request)},
        )

    # Template html of Role page
    def get_template(self):
        return "ors/vendor.html"

    # Service of Role
    def get_service(self):
        return VendorService()
