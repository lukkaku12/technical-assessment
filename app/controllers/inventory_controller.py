from flask import request, jsonify
from app.models.inventory import Inventory
from config import db
from app.services.inventory_service import InventoryService
from flask import render_template

# manual dependency injection
inventory_service = InventoryService(db, Inventory)


def render_create_form():
    return render_template("inventory/create.html")

def create_inventory():
    data = request.form.to_dict()
    try:
        new_item = inventory_service.create(data)
        return render_template("inventory/detail.html", item=new_item), 201
    except Exception as e:
        return render_template("inventory/create.html", error=str(e))


def get_all_inventory():
    items = inventory_service.get_all()
    return render_template('inventory/index.html', inventory=items)

def edit_inventory(item_id):
    item = inventory_service.get_one(item_id)
    if item:
        return render_template("inventory/update.html", item=item)
    else:
        return jsonify({"error": "Item not found"}), 404

def update_inventory(item_id):
    item = inventory_service.get_one(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404

    data = request.form.to_dict()

    try:
        updated_item = inventory_service.update(item, data)
        return render_template("inventory/detail.html", item=updated_item)
    except Exception as e:
        return render_template("inventory/update.html", item=item, error=str(e))

def delete_inventory(item_id):
    item = inventory_service.get_one(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404

    inventory_service.delete(item)
    return jsonify({"message": "Item deleted"}), 200