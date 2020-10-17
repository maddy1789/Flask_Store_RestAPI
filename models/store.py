from db import db

class StoreModel(db.Model):
    __tablename__ = "tbl_stores"

    id = db.Column(db.Integer, primary_key=True)
    store = db.Column(db.String(10))

    items = db.relationship('ItemModel', lazy="dynamic")

    def __init__(self, store):
        self.store = store

    def json(self):
        return {"id": self.id, 
                "store": self.store, 
                "items": [item.json() for item in self.items.all()]
        }

    @classmethod
    def find_by_name(cls, storename):
        return cls.query.filter_by(store = storename).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    