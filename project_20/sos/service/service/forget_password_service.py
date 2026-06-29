from ..models import User
from ..utility.data_validator import DataValidator
from .base_service import BaseService

'''
It contains Role business logics.   
'''


class ForgetPasswordService(BaseService):

    def search(self, params):
        q = self.get_model().objects.filter()

        val = params.get("login", None)
        if (DataValidator.is_not_null(val)):
            q = q.filter(login=val)
        return q

    def get_model(self):
        return User
