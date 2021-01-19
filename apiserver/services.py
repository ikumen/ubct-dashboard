from apiserver.models import User


class BaseService:
    """'Service' layer encapsulation of common datastore model operations.
    """
    __model__ = None

    def init_app(self, app):
        pass

    def _before_update(self, kwargs):
        return kwargs

    def all(self):
        return self.__model__.all()

    def create(self, **kwargs):
        return self.__model__.create(**kwargs)

    def delete(self, id):
        return self.__model__.delete(id)

    def update(self, model=None, id=None, **kwargs):
        if id is None and model is None:
            raise ValueError('Nothing to update, no model or id given')
        if model is None:
            model = self.get(id)
        for k, v in self._before_update(kwargs).items():
            setattr(model, k, v)
        return self.__model__.save(model)

    def get(self, id):
        return self.__model__.get(id)


class UserService(BaseService):
    """Encapsulate `User` model operations.
    """
    __model__ = User


user_service = UserService()