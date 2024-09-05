from app.database.data_layer.base_dao import BaseDAO
from app.models.tests import TestModel


class TestDAO(BaseDAO):
    model = TestModel
