from django.shortcuts import render, redirect

from service.service.ParkingService import ParkingService
from .BaseCtl import BaseCtl



class ParkingListCtl(BaseCtl):

    def request_to_form(self, requestForm):
        self.form['parking_id'] = requestForm.get('parkingId')

    def display(self, request, params={}):
        parking_list = self.get_service().search(self.form)
        self.form['list'] = parking_list
        return render(request, self.get_template(), {'form': self.form})

    def submit(self, request, params={}):

        if request.POST.get('operation', '') == "next":
            self.form['page_number'] = int(request.POST['pageNo'])
            self.form['page_number'] += 1
        if request.POST.get('operation', '') == "previous":
            self.form['page_number'] = int(request.POST['pageNo'])
            self.form['page_number'] -= 1
        if request.POST.get('operation', '') == "search":
            self.form['page_number'] = 1

        Parking_list = self.get_service().search(self.form)
        self.form['list'] = Parking_list
        return render(request, self.get_template(), {'form': self.form})

    def get_service(self):
        return ParkingService()

    def get_template(self):
        return 'ors/parkinglist.html'