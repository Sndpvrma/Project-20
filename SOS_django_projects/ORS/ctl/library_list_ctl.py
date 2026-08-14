from django.shortcuts import render, redirect

from service.service.LibraryService import LibraryService
from .BaseCtl import BaseCtl



class LibraryListCtl(BaseCtl):

    def request_to_form(self, requestForm):
        self.form['library_id'] = requestForm.get('libraryId')

    def display(self, request, params={}):
        library_list = self.get_service().search(self.form)
        self.form['list'] = library_list
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

        library_list = self.get_service().search(self.form)
        self.form['list'] = library_list
        return render(request, self.get_template(), {'form': self.form})

    def get_service(self):
        return LibraryService()

    def get_template(self):
        return 'ors/librarylist.html'