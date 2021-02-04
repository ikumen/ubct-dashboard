
from backend.models import Application, User, SlackUser
from authlib.integrations.flask_client import OAuth
from flask_caching import Cache


class BaseService:
    """'Service' layer encapsulation of common datastore model operations.
    """
    __model__ = None

    def init_app(self, app):
        pass

    def _before_update(self, kwargs):
        return kwargs

    def query(self, **params):
        return self.__model__.query_all(**params)

    def query_with_paging(self, **params):
        return self.__model__.query_all_with_paging(**params)

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

    def find_by_oauth(self, oa_id, oa_provider):
        return self.__model__.query_one(oa_id=oa_id, oa_provider=oa_provider)


class ApplicationService(BaseService):
    """Encapsulates `Application` model operations.
    """
    __model__ = Application

    def all_by_user(self, user_id):
        return self.__model__.query_all(user_id=user_id)

    def delete_by_user(self, id, user_id):
        return self.__model__.delete_by(id=id, user_id=user_id)

    def authorize(self, token):
        return self.__model__.query_one(token=token)
        

class SlackUserService(BaseService):
    __model__ = SlackUser


cache = Cache(config={'CACHE_TYPE': 'simple'})
user_service = UserService()
app_service = ApplicationService()
slackuser_service = SlackUserService()
oauth_service = OAuth()

