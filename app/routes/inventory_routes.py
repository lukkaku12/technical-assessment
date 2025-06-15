from flask import Blueprint
from app.controllers import inventory_controller

inventory_bp = Blueprint('inventory', __name__, url_prefix='/inventory')

# Show create form
inventory_bp.route('/add', methods=['GET'])(inventory_controller.render_create_form)

# Create a new item
inventory_bp.route('/', methods=['POST'])(inventory_controller.create_inventory)

# List all items
inventory_bp.route('/', methods=['GET'])(inventory_controller.get_all_inventory)

# Show edit form
inventory_bp.route('/edit/<int:item_id>', methods=['GET'])(inventory_controller.edit_inventory)

# Update item (using POST from form)
inventory_bp.route('/edit/<int:item_id>', methods=['POST'])(inventory_controller.update_inventory)

# Delete item (using POST from form)
inventory_bp.route('/delete/<int:item_id>', methods=['POST'])(inventory_controller.delete_inventory)