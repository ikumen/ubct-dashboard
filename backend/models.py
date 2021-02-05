from backend.datastores import db
from backend.helpers import JSONSerializer


class BaseModel(JSONSerializer):
    @classmethod
    def _process_params(cls, kwargs):
        return kwargs
        
    @classmethod
    def save(cls, model):
        db.session.add(model)
        db.session.commit()
        return model

    @classmethod
    def create(cls, **kwargs):
        model = cls(**cls._process_params(kwargs))
        return cls.save(model)

    @classmethod
    def delete(cls, id):
        model = cls.query.get(id)
        db.session.delete(model)
        db.session.commit()
        return model

    @classmethod
    def delete_by(cls, **kwargs):
        model = cls.query.filter_by(**kwargs).one()
        db.session.delete(model)
        db.session.commit()
        return model

    @classmethod
    def get(cls, id):
        return cls.query.get(id)

    @classmethod
    def query_one(cls, **kwargs):
        return cls.query.filter_by(**kwargs).first()

    @classmethod
    def query_all(cls, **kwargs):
        query = cls.query
        if kwargs:
            query = query.filter_by(**kwargs)
        return query.all()

    @classmethod
    def query_all_with_paging(cls, page, per_page, sort=None, **kwargs):
        query = cls.query
        if kwargs:
            query = query.filter_by(**kwargs)
        if sort:
            query = query.order_by(sort)
        rv = query.paginate(page=page, per_page=per_page)
        return dict(
            page=page,
            per_page=per_page,
            items=rv.items,
            total=rv.total
        )

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class SlackUser(BaseModel, db.Model):
    __tablename__ = 'sl_users'

    id = db.Column(db.String(11), primary_key=True)
    name = db.Column(db.Unicode(80), nullable=False, index=True)
    full_name = db.Column(db.Unicode(80))
    description = db.Column(db.Unicode(250))
    avatar_id = db.Column(db.String(16))
    tz_offset = db.Column(db.String(9))
    archived_at = db.Column(db.DateTime, nullable=False, index=True)


class SlackChannel(BaseModel, db.Model):
    __tablename__ = 'sl_channels'

    id = db.Column(db.String(11), primary_key=True)
    name = db.Column(db.String(80), nullable=False, index=True)
    description = db.Column(db.Unicode(250))
    archived_at = db.Column(db.DateTime, nullable=False, index=True)


class User(BaseModel, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    oa_id = db.Column(db.String(50), nullable=False, index=True)
    oa_provider = db.Column(db.String(20), nullable=False, index=True)
    name = db.Column(db.String(50), nullable=False, index=True)


class Application(BaseModel, db.Model):
    __tablename__ = 'apps'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False, index=True)
    description = db.Column(db.Unicode(255))
    token = db.Column(db.String(43), nullable=False, index=True)
