
from abc import abstractclassmethod
from backend.models import Application, SlackEmoji, SlackFile, SlackMessage, User, SlackUser, SlackChannel
from authlib.integrations.flask_client import OAuth
from flask_caching import Cache

class BaseService:
    """'Service' layer encapsulation of common datastore model operations.
    """
    __model__ = None

    def init_app(self, app):
        pass

    def create(self, **kwargs):
        return self.__model__.create(**kwargs)

    def find_all_with_paging(self, page, per_page, **kwargs):
        print(f'page={page}, per={per_page}')
        return self.__model__.find_all_with_paging(
            page=page, 
            per_page=per_page,
            **kwargs)


class UserService(BaseService):
    """Encapsulate `User` model operations.
    """
    __model__ = User

    def find_by_oauth(self, oa_id, oa_provider):
        return self.__model__.find_one(oa_id=oa_id, oa_provider=oa_provider, deleted=False)

    def soft_delete(self, id):
        self.__model__.update(id=id, deleted=True)


class ApplicationService(BaseService):
    """Encapsulates `Application` model operations.
    """
    __model__ = Application

    def all_by_user(self, user_id):
        return self.__model__.find_all(user_id=user_id, deleted=False)

    def soft_delete_by_user(self, id, user_id):
        self.__model__.update_by(filters=dict(id=id, user_id=user_id), deleted=True)

    def authorize(self, token):
        return self.__model__.find_one(token=token)
        

class SlackUserService(BaseService):
    __model__ = SlackUser

class SlackChannelService(BaseService):
    __model__ = SlackChannel

class SlackMessageService(BaseService):
    __model__ = SlackMessage

    def get_by_id(self, channel_id, message_id):
        return self.__model__.get(channel_id, message_id)


class SlackEmojiService(BaseService):
    __model__ = SlackEmoji

class SlackFileService(BaseService):
    __model__ = SlackFile


cache = Cache(config={'CACHE_TYPE': 'simple'})

user_service = UserService()
app_service = ApplicationService()

slackuser_service = SlackUserService()
slackchannel_service = SlackChannelService()
slackmessage_service = SlackMessageService()
slackemoji_service = SlackEmojiService()
slackfile_service = SlackFileService()

oauth_service = OAuth()

