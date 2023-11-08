from .. import db


class Point(db.Model):
    id = db.Column(db.Integer(), primary_key=True, nullable=False, unique=True)
    longitude = db.Column(db.Float(), nullable=False)
    latitude = db.Column(db.Float(), nullable=False)

    def json(self):
        return {'id': self.id, 'longitude': self.longitude, 'latitude': self.latitude}
