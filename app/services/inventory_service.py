class InventoryService:
    def __init__(self, db_session, InventoryModel):
        self.db = db_session
        self.Inventory = InventoryModel

    def create(self, data):
        new_item = self.Inventory(**data)
        self.db.session.add(new_item)
        self.db.session.commit()
        return new_item

    def get_all(self):
        return self.Inventory.query.all()

    def get_one(self, item_id):
        return self.Inventory.query.get(item_id)

    def update(self, item, data):
        for key, value in data.items():
            setattr(item, key, value)
        self.db.session.commit()
        return item

    def delete(self, item):
        self.db.session.delete(item)
        self.db.session.commit()