from service.models import User, Role
from .BaseDAO import BaseDAO


class ForgetPasswordDAO(BaseDAO):

    def get_model(self):
        return User

    def get_Unique(self):
        return ["login"]

    def populate(self, obj):
        try:
            role = Role.objects.get(id=obj.role_id)
            obj.role_Name = role.name
        except Role.DoesNotExist:
            obj.role_Name = ""
        return obj
