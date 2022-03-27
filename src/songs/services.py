from django.db import connections


class BaseService:
    @staticmethod
    def last_query():
        print(connections["default"].queries)

    class Meta:
        abstract = True
