from ..models import Marksheet
from ..utility.data_validator import DataValidator
from .base_service import BaseService
from django.core.paginator import Paginator


class MarksheetService(BaseService):

    def search(self, params):

        page_no = int(params.get("page_no", 1))
        page_size = self.pageSize

        query = self.get_model().objects.all()

        value = params.get("roll_number", None)
        if DataValidator.is_not_null(value):
            query = query.filter(roll_number__istartswith=value.strip())

        value = params.get("name", None)
        if DataValidator.is_not_null(value):
            query = query.filter(name__istartswith=value.strip())

        value = params.get("physics", None)
        if DataValidator.is_not_null(value):
            query = query.filter(physics=value)

        value = params.get("chemistry", None)
        if DataValidator.is_not_null(value):
            query = query.filter(chemistry=value)

        value = params.get("maths", None)
        if DataValidator.is_not_null(value):
            query = query.filter(maths=value)

        value = params.get("student_id", None)
        if DataValidator.is_not_null(value) and str(value) != "0":
            query = query.filter(student_id=value)

        paginator = Paginator(query, page_size)

        page_obj = paginator.get_page(page_no)

        params["has_next"] = page_obj.has_next()
        params["has_previous"] = page_obj.has_previous()
        params["start_index"] = (page_no - 1) * page_size

        return page_obj

    def get_model(self):
        return Marksheet
