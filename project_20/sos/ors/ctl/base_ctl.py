import logging
from abc import ABC, abstractmethod
from django.http import HttpResponse
from django.shortcuts import render

logger = logging.getLogger(__name__)

class BaseCtl(ABC):

    def __init__(self):
        self.page_list = []
        self.preload_data = {}
        self.form = {
            "id": 0,
            "message": "",
            "error": False,
            "input_error": {},
            "page_no": 1
        }

    def execute(self, request, params={}):
        logger.info("%s.execute() method=%s params=%s", self.__class__.__name__, request.method, params)

        if "delete" == params.get("action"):
            id: int = params.get("id")
            self.get_service().delete(id)
            logger.info("%s deleted id=%s", self.__class__.__name__, id)

        if "GET" == request.method:
            return self.display(request, params)
        elif "POST" == request.method:
            self.request_to_form(request.POST)
            if self.input_validation():
                logger.warning("%s.input_validation() failed form=%s", self.__class__.__name__, self.form)
                return render(request, self.get_template(),{"form": self.form, "preload_data": self.preload(request)},)
            else:
                return self.submit(request, params)
        else:
            logger.error("%s unsupported request method=%s", self.__class__.__name__, request.method)
            message = "Request is not supported"
            return HttpResponse(message)

    def preload(self, request):
        return self.preload_data

    def input_validation(self):
        self.form["error"] = False
        self.form["message"] = ""
        self.form["input_error"] = {}

    def request_to_form(self, request_form):
        pass

    def form_to_model(self, obj):
        pass

    def model_to_form(self, obj):
        pass

    @abstractmethod
    def display(self, request, params={}):
        pass

    @abstractmethod
    def submit(self, request, params={}):
        pass

    @abstractmethod
    def get_service(self):
        pass

    @abstractmethod
    def get_template(self):
        pass
