from flask import request, jsonify, render_template, url_for
from app.models.inventory import Inventory
from config import db
from app.services.inventory_service import InventoryService
from sqlalchemy.exc import SQLAlchemyError

inventory_service = InventoryService(db, Inventory)

def render_create_form():
    return render_template("inventory/create.html")

def create_inventory():
    data = request.form.to_dict()
    try:
        if not data.get('name') or not data.get('quantity'):
            return render_template(
                "inventory/create.html",
                error="Nombre y cantidad son campos obligatorios"
            ), 400
            
        new_item = inventory_service.create(data)
        
        
        return render_template("inventory/detail.html", item=new_item), 201
    except (ValueError, TypeError) as e:
        return render_template("inventory/create.html", error=str(e)), 400
    except SQLAlchemyError as e:
        return render_template("inventory/create.html", error="Error en base de datos"), 500
    except Exception as e:
        return render_template("inventory/create.html", error="Error inesperado"), 500

def get_all_inventory():
    try:
        items = inventory_service.get_all()
        return render_template('inventory/index.html', inventory=items)
    except SQLAlchemyError as e:
        
        
        return render_template('inventory/index.html', 
                             inventory=[], 
                             error="Error al cargar el inventario"), 500

def edit_inventory(item_id):
    try:
        item = inventory_service.get_one(item_id)
        if not item:
            
            
            return render_template(
                "errors/404.html",
                message=f"Ítem con ID {item_id} no encontrado",
                redirect_url=url_for('inventory.get_all_inventory')
            ), 404
            
        return render_template("inventory/update.html", item=item)
    except SQLAlchemyError as e:
        
        return render_template(
            "errors/500.html",
            message="Error de base de datos",
            redirect_url=url_for('inventory.get_all_inventory')
        ), 500

def update_inventory(item_id):
    try:
        item = inventory_service.get_one(item_id)
        if not item:
            return render_template(
                "errors/404.html",
                message=f"No se puede actualizar - Ítem con ID {item_id} no encontrado",
                redirect_url=url_for('inventory.get_all_inventory')
            ), 404
        
        data = request.form.to_dict()
        if not data.get('name') or not data.get('quantity'):
            return render_template(
                "inventory/update.html",
                item=item,
                error="Nombre y cantidad son campos obligatorios"
            ), 400
            
        updated_item = inventory_service.update(item, data)
        
        return render_template("inventory/detail.html", item=updated_item)
    except (ValueError, TypeError) as e:
        return render_template("inventory/update.html", item=item, error=str(e)), 400
    except SQLAlchemyError as e:
        return render_template("inventory/update.html", item=item, error="Error en base de datos"), 500

def delete_inventory(item_id):
    try:
        item = inventory_service.get_one(item_id)
        if not item:
            return jsonify({
                "success": False,
                "message": f"El ítem con ID {item_id} no existe"
            }), 404
            
        inventory_service.delete(item)
        return jsonify({
            "success": True,
            "message": "Ítem eliminado exitosamente",
            "deleted_id": item_id
        }), 200
    except SQLAlchemyError as e:
        return jsonify({
            "success": False,
            "message": "Error de base de datos al eliminar"
        }), 500
    except Exception as e:
        return jsonify({
            "success": False,
            "message": "Error inesperado en el servidor"
        }), 500