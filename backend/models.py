from enum import unique

from sqlalchemy.sql.schema import ForeignKeyConstraint
from backend.datastores import db
from backend.helpers import JSONSerializer


class BaseModel(JSONSerializer):
    __json_exclude__ = []
    __default_sort__ = None

    @classmethod
    def save(cls, model):
        """Persist the given model to underlying datastore.
        """
        db.session.add(model)
        db.session.commit()
        return model

    @classmethod
    def create(cls, **kwargs):
        """Creates an instance of the implementing model and persists it
        to the underlying datastore.
        """
        model = cls(**kwargs)
        return cls.save(model)

    @classmethod
    def delete(cls, id):
        """Delete the model with the given id from the underlying datastore.
        """
        model = cls.query.get(id)
        db.session.delete(model)
        db.session.commit()
        return model

    @classmethod
    def delete_by(cls, **kwargs):
        """Delete the model specified by the given parameters from 
        the underlying datastore.
        """
        model = cls.get_by(**kwargs)
        db.session.delete(model)
        db.session.commit()
        return model

    @classmethod
    def get(cls, id):
        """Return the model with the given id from the underlying datastore.
        """
        return cls.query.get(id)

    @classmethod
    def find_one(cls, **kwargs):
        """Return the model specified by the given parameters from the 
        underlying datastore.
        """
        model = cls.query.filter_by(**kwargs).first()
        return model

    @classmethod
    def _prepare_query(cls, sort=None, sort_dir=None, **kwargs):
        query = cls.query
        if kwargs:
            query = query.filter_by(**kwargs)
        if sort:
            query = query.order_by(getattr(getattr(cls, sort), sort_dir)())
        elif cls.__default_sort__:
            query = query.order_by(cls.__default_sort__)
        return query

    @classmethod
    def find_all(cls, **kwargs):
        """Find and return list of models specified by the given parameters
        from the underlying datastore.
        """
        query = cls._prepare_query(**kwargs)
        return query.all()

    @classmethod
    def find_all_with_paging(cls, page, per_page, **kwargs):
        """Find and return list of models specified by the given parameters
        from the underlying datastore. Results are paged back and controlled
        via the page and per_page parameters.
        """
        query = cls._prepare_query(**kwargs)
        rv = query.paginate(page=page, per_page=per_page)
        return dict(
            page=page,
            per_page=per_page,
            items=rv.items,
            total=rv.total
        )

    @classmethod
    def update(cls, id, **kwargs):
        """Update the model with the given id with passed in parameters
        to the underlying datastore.
        """
        cls.update_by(filters={'id': id}, **kwargs)

    @classmethod
    def update_by(cls, filters, **kwargs):
        """Update the model specified by the filter parameters with passed 
        in parameters to the underlying datastore.
        """
        cls.query.filter_by(**filters).update(kwargs)
        db.session.commit()

    def to_json(self):
        """Returns a json serializable representation (e.g, dict) of this model.
        """ 
        rv = {}
        # https://docs.sqlalchemy.org/en/13/orm/mapping_api.html#sqlalchemy.orm.Mapper.iterate_properties
        for prop in self.__mapper__.iterate_properties:
            if prop.key not in self.__json_exclude__:
                rv[prop.key] = getattr(self, prop.key)
        return rv


class SlackUser(BaseModel, db.Model):
    __tablename__ = 'sl_users'
    __default_sort__ = 'name'
    __json_exclude__ = ['archived_at']

    id = db.Column(db.String(11), primary_key=True)
    name = db.Column(db.Unicode(80), nullable=False, index=True)
    full_name = db.Column(db.Unicode(80))
    description = db.Column(db.Unicode(250))
    avatar_id = db.Column(db.String(16))
    tz_offset = db.Column(db.String(9))
    archived_at = db.Column(db.DateTime, nullable=False, index=True)


class SlackChannel(BaseModel, db.Model):
    __tablename__ = 'sl_channels'
    __default_sort__ = 'name'
    __json_exclude__ = ['archived_at']

    id = db.Column(db.String(11), primary_key=True)
    name = db.Column(db.String(80), nullable=False, index=True)
    description = db.Column(db.Unicode(250))
    archived_at = db.Column(db.DateTime, nullable=False, index=True)


class SlackMessage(BaseModel, db.Model):
    __tablename__ = 'sl_messages'
    __default_sort__ = 'id'
    __json_exclude__ = ['deleted']


    id = db.Column(db.String(17), primary_key=True)
    channel_id = db.Column(db.ForeignKey('sl_channels.id'), primary_key=True)
    thread_id = db.Column(db.String(17), index=True)
    content = db.Column(db.UnicodeText(None))
    user_id = db.Column(db.ForeignKey('sl_users.id'), index=True)
    deleted = db.Column(db.Boolean, index=True)

    files = db.relationship('SlackFile', foreign_keys='SlackFile.message_id,SlackFile.channel_id', lazy='subquery')
    reactions = db.relationship('SlackReaction', foreign_keys='SlackReaction.message_id,SlackReaction.channel_id', lazy='subquery')

class SlackFile(BaseModel, db.Model):
    __tablename__ = 'sl_files'
    __default_sort__ = 'channel_id'
    __json_exclude__ = ['message_id', 'channel_id']

    message_id = db.Column(db.ForeignKey('sl_messages.id'), primary_key=True)
    channel_id = db.Column(db.ForeignKey('sl_messages.channel_id'), primary_key=True)
    url = db.Column(db.String(2048), nullable=False, primary_key=True)
    
    __table_args__ = (
        ForeignKeyConstraint([message_id, channel_id],
                             [SlackMessage.id, SlackMessage.channel_id]),
    )


class SlackEmoji(BaseModel, db.Model):
    __tablename__ = 'sl_emojis'
    __default_sort__ = 'id'

    id = db.Column(db.String(255), primary_key=True)
    url = db.Column(db.String(2048), nullable=False, index=True)


class SlackReaction(BaseModel, db.Model):
    __tablename__ = 'sl_reactions'
    __default_sort__ = 'user_id'
    __json_exclude__ = ['message_id', 'channel_id']

    message_id = db.Column(db.ForeignKey('sl_messages.id'), primary_key=True)
    channel_id = db.Column(db.ForeignKey('sl_messages.channel_id'), primary_key=True)
    user_id = db.Column(db.String(11), primary_key=True)
    emoji_id = db.Column(db.String(255), primary_key=True)

    __table_args__ = (
        ForeignKeyConstraint([message_id, channel_id],
                             [SlackMessage.id, SlackMessage.channel_id]),
    )


class User(BaseModel, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    oa_id = db.Column(db.String(50), nullable=False, index=True)
    oa_provider = db.Column(db.String(20), nullable=False, index=True)
    name = db.Column(db.String(50), nullable=False, index=True)
    deleted = db.Column(db.Boolean, index=True, nullable=False, default=False)


class Application(BaseModel, db.Model):
    __tablename__ = 'apps'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False, index=True)
    description = db.Column(db.Unicode(255))
    token = db.Column(db.String(43), nullable=False, index=True)
    deleted = db.Column(db.Boolean, index=True, nullable=False, default=False)
