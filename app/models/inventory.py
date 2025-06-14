from config import db

class Inventory(db.Model):
    __tablename__ = 'inventory'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Numeric, nullable=False)
    mac_address = db.Column(db.String(50), nullable=False)
    serial_number = db.Column(db.String(100), nullable=False)
    manufacturer = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(150), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": str(self.price),
            "mac_address": self.mac_address,
            "serial_number": self.serial_number,
            "manufacturer": self.manufacturer,
            "description": self.description
        }