from flask import Blueprint
from app.controllers import inventory_controller

inventory_bp = Blueprint('inventory', __name__, url_prefix='/inventory')

inventory_bp.route('/', methods=['POST'])(inventory_controller.create_inventory)
inventory_bp.route('/', methods=['GET'])(inventory_controller.get_all_inventory)
inventory_bp.route('/<int:item_id>', methods=['GET'])(inventory_controller.get_inventory)
inventory_bp.route('/<int:item_id>', methods=['PUT'])(inventory_controller.update_inventory)
inventory_bp.route('/<int:item_id>', methods=['DELETE'])(inventory_controller.delete_inventory)