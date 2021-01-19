from apiserver.datastores import db


class BaseModel:
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
    def all(cls):
        return [model for model in cls.query.all()]

    @classmethod
    def delete(cls, id):
        model = cls.query.get(id)
        db.session.delete(model)
        db.session.commit()
        return model

    @classmethod
    def get(cls, id):
        return cls.query.get(id)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class User(BaseModel, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(11), primary_key=True)
    name = db.Column(db.Unicode(80), nullable=False, index=True)
    full_name = db.Column(db.Unicode(80))
    description = db.Column(db.Unicode(250))
    timezone = db.Column(db.String(9))
    avatar_id = db.Column(db.String(16))
    archived_at = db.Column(db.DateTime, nullable=False, index=True)
