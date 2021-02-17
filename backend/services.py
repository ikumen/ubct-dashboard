
from azure.storage.blob import generate_container_sas, ContainerSasPermissions, BlobSasPermissions, BlobServiceClient
from authlib.integrations.flask_client import OAuth
from flask_caching import Cache
from datetime import datetime, timedelta, timezone

from backend.models import Application, SlackEmoji, SlackFile, SlackMessage, SlackReaction, User, SlackUser, SlackChannel


cache = Cache(config={'CACHE_TYPE': 'simple'})


class StorageService:
    def init_app(self, app):
        self.account_name = app.config['BLOB_ACCOUNT_NAME']
        self.dataset_container_name = app.config['BLOB_DATASET_CONTAINER_NAME']
        self.account_key = app.config['BLOB_ACCOUNT_KEY']
        self.endpoint_host = app.config['BLOB_ENDPOINT_HOST']

        conn_str = f'DefaultEndpointsProtocol=https;AccountName={self.account_name};AccountKey={self.account_key};EndpointSuffix={self.endpoint_host}'
        blob_service = BlobServiceClient.from_connection_string(conn_str=conn_str)
        self.container_client = blob_service.get_container_client(container=self.dataset_container_name)

    @cache.cached(timeout=7200)
    def list_dataset_container_files(self):
        datafiles = []
        for blob in self.container_client.list_blobs():
            datafiles.append(dict(
                size=((blob['size'] // 100000) / 10), 
                name=blob['name']
            ))
        return datafiles

    @cache.memoize(timeout=1200)
    def get_url_for_dataset_file(self, file_name):
        sas_token = generate_container_sas(
            account_name=self.account_name,
            container_name=self.dataset_container_name,
            account_key=self.account_key,
            permission=ContainerSasPermissions(read=True, list=True),
            expiry=datetime.now(timezone.utc) + timedelta(minutes=20))
        return f'https://{self.account_name}.blob.{self.endpoint_host}/{self.dataset_container_name}/{file_name}?{sas_token}'



class BaseService:
    """'Service' layer encapsulation of common datastore model operations.
    """
    __model__ = None

    def init_app(self, app):
        pass

    def count(self):
        return self.__model__.count()

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

class SlackReactionService(BaseService):
    __model__ = SlackReaction


user_service = UserService()
app_service = ApplicationService()

storage_service = StorageService()

slackuser_service = SlackUserService()
slackchannel_service = SlackChannelService()
slackmessage_service = SlackMessageService()
slackemoji_service = SlackEmojiService()
slackfile_service = SlackFileService()
slackreaction_service = SlackReactionService()

oauth_service = OAuth()

