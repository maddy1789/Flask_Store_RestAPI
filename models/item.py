from db import db

class ItemModel(db.Model):
    __tablename__ = "tbl_items"

    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(10))
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey('tbl_stores.id'))
    store = db.relationship('StoreModel')

    def __init__(self, item, price, store_id):
        self.item = item
        self.price = price
        self.store_id = store_id

    def json(self):
        return {"item": self.item, "password": self.price}

    @classmethod
    def find_by_name(cls, itemname):
        return cls.query.filter_by(item = itemname).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()