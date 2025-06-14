from flask import request, jsonify
from app.models.inventory import Inventory
from config import db
from app.services.inventory_service import InventoryService
from flask import render_template

# Inyección manual de dependencias
inventory_service = InventoryService(db, Inventory)

def create_inventory():
    data = request.get_json()
    try:
        new_item = inventory_service.create(data)
        return jsonify(new_item.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


def get_all_inventory():
    items = inventory_service.get_all()
    return render_template('inventory/index.html', inventory=items)

def get_inventory(item_id):
    item = inventory_service.get_one(item_id)
    if item:
        return jsonify(item.to_dict())
    return jsonify({"error": "Item not found"}), 404

def update_inventory(item_id):
    item = inventory_service.get_one(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404

    data = request.get_json()
    try:
        updated = inventory_service.update(item, data)
        return jsonify(updated.to_dict())
    except Exception as e:
        return jsonify({"error": str(e)}), 400

def delete_inventory(item_id):
    item = inventory_service.get_one(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404

    inventory_service.delete(item)
    return jsonify({"message": "Item deleted"}), 200