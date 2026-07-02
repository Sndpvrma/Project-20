from ..models import Manager
from ..utility.data_validator import DataValidator
from .base_service import BaseService
from django.core.paginator import Paginator

'''
It contains Broker business logics.   
'''


class ManagerService(BaseService):

    def search(self, params):

        page_no = int(params.get("page_no", 0))
        page_size = self.pageSize

        query = self.get_model().objects.all()

        if page_no == 0:
            return query

        value = params.get("manager_name", None)
        if DataValidator.is_not_null(value):
            query = query.filter(manager_name__istartswith=value.strip())

        value = params.get("branch_name", None)
        if DataValidator.is_not_null(value):
            query = query.filter(branch_name__istartswith=value.strip())

        value = params.get("contact_number", None)
        if DataValidator.is_not_null(value):
            query = query.filter(contact_number__istartswith=value.strip())


        paginator = Paginator(query, page_size)

        page_obj = paginator.get_page(page_no)

        params["has_next"] = page_obj.has_next()
        params["has_previous"] = page_obj.has_previous()
        params["start_index"] = (page_no - 1) * page_size

        return page_obj

    def get_model(self):
        return Manager