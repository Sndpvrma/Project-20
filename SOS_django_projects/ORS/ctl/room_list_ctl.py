from django.shortcuts import render
from .BaseCtl import BaseCtl
from service.service.RoomService import RoomService


class RoomListCtl(BaseCtl):

    def request_to_form(self, requestForm):
        self.form["room_id"] = requestForm.get("roomId", None)
        self.form["page_number"] = int(requestForm.get("page_number", 1))

    def display(self, request, params={}):
        self.page_list = self.get_service().search(self.form, page_number=1)
        res = render(
            request,
            self.get_template(),
            {"pageList": self.page_list, "form": self.form, "preload_data": self.preload(request)},
        )
        return res

    def submit(self, request, params={}):
        self.request_to_form(request.POST)
        page_number = self.form.get("page_number", 1)
        self.page_list = self.get_service().search(self.form, page_number=page_number)
        res = render(
            request,
            self.get_template(),
            {"pageList": self.page_list, "form": self.form, "preload_data": self.preload(request)},
        )
        return res

    def get_template(self):
        return "ors/roomlist.html"

    def get_service(self):
        return RoomService()