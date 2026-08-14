from service.dao.LibraryDAO import LibraryDAO
from service.service.BaseService import BaseService


class LibraryService(BaseService):
    def get_dao(self):
        return LibraryDAO()