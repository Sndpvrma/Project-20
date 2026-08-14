from django.shortcuts import render

from ORS.ctl.BaseCtl import BaseCtl
from ORS.utility.HtmlUtility import HtmlUtility
from service.models import Library
from service.service.LibraryService import LibraryService
from service.utility.DataValidator import DataValidator


class LibraryCtl(BaseCtl):

    def preload(self, request):
        # Also make preload available under form for templates using `form.preload_data`
        self.form["preload_data"] = self.preload_data
        return self.preload_data

    # Populate Form from HTTP Request
    def request_to_form(self, request):
        self.form["id"] = request.get("id", 0)
        print('R2F =====================>', self.form["id"])
        self.form["library_id"] = request.get("libraryId", 0)
        self.form["library_name"] = request.get("libraryName", "")
        self.form["address"] = request.get("address", "")
        self.form["total_books"] = request.get("totalBooks", "")
        self.form["contact_no"] = request.get("contactNo", "")

    # Populate Form from Model
    def model_to_form(self, obj):
        if obj == None:
            return
        self.form["id"] = obj.id
        # print('M2F======================>', self.form["id"])
        self.form["library_id"] = obj.library_id
        self.form["library_name"] = obj.library_name
        self.form["address"] = obj.address
        self.form["total_books"] = obj.total_books
        self.form["contact_no"] = obj.contact_no
        print('M2F======================>', self.form["contact_no"])


    # Convert form into module
    def form_to_model(self, obj):
        pk = int(self.form.get("id", 0))
        if pk > 0:
            obj.id = pk
        print('F2M======================>', obj.id)
        obj.library_id = int(self.form.get("library_id", 0))
        obj.library_name = self.form.get("library_name", "")
        obj.address = self.form.get("address", "")
        obj.total_books = self.form.get("total_books", "")
        obj.contact_no = self.form.get("contact_no", "")
        return obj

    # Validate form
    def input_validation(self):
        super().input_validation()
        inputError = self.form["inputError"]
        if DataValidator.isNull(self.form["library_id"]):
            inputError["library_id"] = "Library Id is required"
            self.form["error"] = True
        if DataValidator.isNull(self.form["library_name"]):
            inputError["library_name"] = "Library Name is required"
            self.form["error"] = True
        if DataValidator.isNull(self.form["address"]):
            inputError["address"] = "Address is required"
            self.form["error"] = True
        if DataValidator.isNull(self.form["total_books"]):
            inputError["total_books"] = "Total Books is required"
            self.form["error"] = True
        if DataValidator.isNull(self.form["contact_no"]):
            inputError["contact_no"] = "Contact No is required"
            self.form["error"] = True
        return self.form["error"]

    # Display Role page
    def display(self, request, params={}):
        if params["id"] > 0:
            library = self.get_service().get(params["id"])
            self.model_to_form(library)
        return render(
            request,
            self.get_template(),
            {"form": self.form, "preload_data": self.preload(request)},
        )

    # Submit Role page
    def submit(self, request, _params={}):
        library = self.form_to_model(Library())
        self    .get_service().save(library)
        if int(self.form["id"]) > 0:
            self.form["id"] = library.id
        self.form["error"] = False
        self.form["message"] = "Data is saved"
        return render(
            request,
            self.get_template(),
            {"form": self.form, "preload_data": self.preload(request)},
        )

    # Template html of Role page
    def get_template(self):
        return "ors/library.html"

    # Service of Role
    def get_service(self):
        return LibraryService()
