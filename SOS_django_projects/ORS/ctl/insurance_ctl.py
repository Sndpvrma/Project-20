from django.shortcuts import render

from ORS.ctl.BaseCtl import BaseCtl
from ORS.utility.HtmlUtility import HtmlUtility
from service.models import Insurance
from service.service.InsuranceService import InsuranceService
from service.utility.DataValidator import DataValidator


class InsuranceCtl(BaseCtl):

    def preload(self, request):
        return self.preload_data

    # Populate Form from HTTP Request
    def request_to_form(self, request):
        self.form["id"] = request.get("id", 0)
        print('R2F =====================>', self.form["id"])
        self.form["policy_id"] = request.get("policyId", 0)
        self.form["policy_holder_name"] = request.get("policyHolderName", "")
        self.form["policy_type"] = request.get("policyType", "")
        self.form["premium_amount"] = request.get("premiumAmount", "")
        self.form["expiry_date"] = request.get("expiryDate", "")

    # Populate Form from Model
    def model_to_form(self, obj):
        if obj == None:
            return
        self.form["id"] = obj.id
        # print('M2F======================>', self.form["id"])
        self.form["policy_id"] = obj.policy_id
        self.form["policy_holder_name"] = obj.policy_holder_name
        self.form["policy_type"] = obj.policy_type
        self.form["premium_amount"] = obj.premium_amount
        self.form["expiry_date"] = obj.expiry_date
        print('M2F======================>', self.form["expiry_date"])


    # Convert form into module
    def form_to_model(self, obj):
        pk = int(self.form.get("id", 0))
        if pk > 0:
            obj.id = pk
        print('F2M======================>', obj.id)
        obj.policy_id = int(self.form.get("policy_id", 0))
        obj.policy_holder_name = self.form.get("policy_holder_name", "")
        obj.policy_type = self.form.get("policy_type", "")
        obj.premium_amount = self.form.get("premium_amount", "")
        obj.expiry_date = self.form.get("expiry_date", "")
        return obj

    # Validate form
    def input_validation(self):
        super().input_validation()
        inputError = self.form["inputError"]
        if DataValidator.isNull(self.form["policy_id"]):
            inputError["policy_id"] = "Policy Id is required"
            self.form["error"] = True
        if DataValidator.isNull(self.form["policy_holder_name"]):
            inputError["policy_holder_name"] = "Policy Holder Name is required"
            self.form["error"] = True
        if DataValidator.isNull(self.form["policy_type"]):
            inputError["policy_type"] = "Policy Type is required"
            self.form["error"] = True
        if DataValidator.isNull(self.form["premium_amount"]):
            inputError["premium_amount"] = "Premium Amount is required"
            self.form["error"] = True
        if DataValidator.isNull(self.form["expiry_date"]):
            inputError["expiry_date"] = "Expiry Date is required"
            self.form["error"] = True
        return self.form["error"]

    # Display Role page
    def display(self, request, params={}):
        if params["id"] > 0:
            insurance = self.get_service().get(params["id"])
            self.model_to_form(insurance)
        return render(
            request,
            self.get_template(),
            {"form": self.form, "preload_data": self.preload(request)},
        )

    # Submit Role page
    def submit(self, request, _params={}):
        insurance = self.form_to_model(Insurance())
        self    .get_service().save(insurance)
        if int(self.form["id"]) > 0:
            self.form["id"] = insurance.id
        self.form["error"] = False
        self.form["message"] = "Data is saved"
        return render(
            request,
            self.get_template(),
            {"form": self.form, "preload_data": self.preload(request)},
        )

    # Template html of Role page
    def get_template(self):
        return "ors/insurance.html"

    # Service of Role
    def get_service(self):
        return InsuranceService()
