from django.shortcuts import render, redirect

from service.service.HotelService import HotelService
from .BaseCtl import BaseCtl



class HotelListCtl(BaseCtl):

    def request_to_form(self, requestForm):
        self.form['hotel_id'] = requestForm.get('hotelId')

    def display(self, request, params={}):
        hotel_list = self.get_service().search(self.form)
        self.form['list'] = hotel_list
        return render(request, self.get_template(), {'form': self.form})

    def submit(self, request, params={}):

        if request.POST.get('operation', '') == "next":
            self.form['page_number'] = int(request.POST['pageNumber'])
            self.form['page_number'] += 1
        if request.POST.get('operation', '') == "previous":
            self.form['page_number'] = int(request.POST['pageNumber'])
            self.form['page_number'] -= 1
        if request.POST.get('operation', '') == "search":
            self.form['page_number'] = 1

        hotel_list = self.get_service().search(self.form)
        self.form['list'] = hotel_list
        return render(request, self.get_template(), {'form': self.form})

    def get_service(self):
        return HotelService()

    def get_template(self):
        return 'ors/hotellist.html'