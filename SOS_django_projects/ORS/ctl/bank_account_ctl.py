from django.shortcuts import render

from ORS.ctl.BaseCtl import BaseCtl
from ORS.utility.HtmlUtility import HtmlUtility
from service.models import BankAccount
from service.service.BankAccountService import BankAccountService
from service.utility.DataValidator import DataValidator


class BankAccountCtl(BaseCtl):

    def preload(self, request):
        # Also make preload available under form for templates using `form.preload_data`
        self.form["preload_data"] = self.preload_data
        return self.preload_data

    # Populate Form from HTTP Request
    def request_to_form(self, request):
        self.form["id"] = request.get("id", 0)
        print('R2F =====================>', self.form["id"])
        self.form["account_number"] = request.get("accountNumber", 0)
        self.form["account_holder_name"] = request.get("accountHolderName", "")
        self.form["account_type"] = request.get("accountType", "")
        self.form["balance"] = request.get("balance", 0.0)
        self.form["branch_name"] = request.get("branchName", "")

    # Populate Form from Model
    def model_to_form(self, obj):
        if obj == None:
            return
        self.form["id"] = obj.id
        # print('M2F======================>', self.form["id"])
        self.form["account_number"] = obj.account_number
        self.form["account_holder_name"] = obj.account_holder_name
        self.form["account_type"] = obj.account_type
        self.form["balance"] = obj.balance
        self.form["branch_name"] = obj.branch_name
        print('M2F======================>', self.form["branch_name"])


    # Convert form into module
    def form_to_model(self, obj):
        pk = int(self.form.get("id", 0))
        if pk > 0:
            obj.id = pk
        print('F2M======================>', obj.id)
        obj.account_number = int(self.form.get("account_number", 0))
        obj.account_holder_name = self.form.get("account_holder_name", "")
        obj.account_type = self.form.get("account_type", "")
        obj.balance = self.form.get("balance", 0.0)
        obj.branch_name = self.form.get("branch_name", "")
        return obj

    # Validate form
    def input_validation(self):
        super().input_validation()
        inputError = self.form["inputError"]
        if DataValidator.isNull(self.form["account_number"]):
            inputError["account_number"] = "Account Number is required"
            self.form["error"] = True
        if DataValidator.isNull(self.form["account_holder_name"]):
            inputError["account_holder_name"] = "Account Holder Name is required"
            self.form["error"] = True
        if DataValidator.isNull(self.form["account_type"]):
            inputError["account_type"] = "Account Type is required"
            self.form["error"] = True
        if DataValidator.isNull(self.form["balance"]):
            inputError["balance"] = "Balance is required"
            self.form["error"] = True
        if DataValidator.isNull(self.form["branch_name"]):
            inputError["branch_name"] = "Branch Name is required"
            self.form["error"] = True
        return self.form["error"]

    # Display Role page
    def display(self, request, params={}):
        if params["id"] > 0:
            bank_account = self.get_service().get(params["id"])
            self.model_to_form(bank_account)
        return render(
            request,
            self.get_template(),
            {"form": self.form, "preload_data": self.preload(request)},
        )

    # Submit Role page
    def submit(self, request, _params={}):
        bank_account = self.form_to_model(BankAccount())
        self    .get_service().save(bank_account)
        if int(self.form["id"]) > 0:
            self.form["id"] = bank_account.id
        self.form["error"] = False
        self.form["message"] = "Data is saved"
        return render(
            request,
            self.get_template(),
            {"form": self.form, "preload_data": self.preload(request)},
        )

    # Template html of Role page
    def get_template(self):
        return "ors/bankaccount.html"

    # Service of Role
    def get_service(self):
        return BankAccountService()
