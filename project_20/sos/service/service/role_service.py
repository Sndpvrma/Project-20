from ..models import Role
from ..utility.data_validator import DataValidator
from .base_service import BaseService
from django.core.paginator import Paginator

'''
It contains Role business logics.   
'''


class RoleService(BaseService):

    def search(self, params):

        page_no = int(params.get("page_no", 0))
        page_size = self.pageSize

        query = self.get_model().objects.all()

        if page_no == 0:
            return query

        value = params.get("name", None)
        if DataValidator.is_not_null(value):
            query = query.filter(name__istartswith=value.strip())

        value = params.get("description", None)
        if DataValidator.is_not_null(value):
            query = query.filter(description__istartswith=value.strip())

        paginator = Paginator(query, page_size)

        page_obj = paginator.get_page(page_no)

        params["has_next"] = page_obj.has_next()
        params["has_previous"] = page_obj.has_previous()
        params["start_index"] = (page_no - 1) * page_size

        return page_obj

    def get_model(self):
        return Role
