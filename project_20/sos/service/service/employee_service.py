from ..models import Employee
from ..utility.data_validator import DataValidator
from .base_service import BaseService
from django.core.paginator import Paginator

"""
It contains User business logics.   
"""


class EmployeeService(BaseService):

    def authenticate(self, params):
        employee_list = self.search(params)
        if len(employee_list) > 0:
            return employee_list[0]
        else:
            return None

    def search(self, params):

        page_no = int(params.get("page_no", 0))
        page_size = self.pageSize

        query = self.get_model().objects.all()

        if page_no == 0:
            return query

        value = params.get("patient_name", None)
        if DataValidator.is_not_null(value):
            query = query.filter(employee_name__istartswith=value.strip())

        value = params.get("disease", None)
        if DataValidator.is_not_null(value):
            query = query.filter(department__istartswith=value.strip())

        value = params.get("doctor_name", None)
        if DataValidator.is_not_null(value):
            query = query.filter(salary__istartswith=value.strip())

        value = params.get("age", None)
        if DataValidator.is_not_null(value) and str(value) != "0":
            query = query.filter(joining_date__istartswith=value.strip())

        paginator = Paginator(query, page_size)

        page_obj = paginator.get_page(page_no)

        params["has_next"] = page_obj.has_next()
        params["has_previous"] = page_obj.has_previous()
        params["start_index"] = (page_no - 1) * page_size

        return page_obj

    def get_model(self):
        return Employee
