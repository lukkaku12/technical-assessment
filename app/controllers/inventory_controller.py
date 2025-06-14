from flask import request, jsonify, redirect, url_for, flash, render_template
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
        flash(f"Ítem '{new_item.name}' creado exitosamente!", 'success')
        return redirect(url_for('inventory.get_all_inventory'))
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
        flash("Error al cargar el inventario", 'danger')
        return render_template('inventory/index.html', inventory=[]), 500

def edit_inventory(item_id):
    
    try:
        item = inventory_service.get_one(item_id)
        if not item:
            flash("Ítem no encontrado", 'warning')
            return redirect(url_for('inventory.get_all_inventory'))
            
        return render_template("inventory/update.html", item=item)
    except SQLAlchemyError as e:
        flash("Error de base de datos", 'danger')
        return redirect(url_for('inventory.get_all_inventory'))

def update_inventory(item_id):
    
    try:
        item = inventory_service.get_one(item_id)
        if not item:
            flash("Ítem no encontrado", 'warning')
            return redirect(url_for('inventory.get_all_inventory'))
        
        data = request.form.to_dict()
        
        
        if not data.get('name') or not data.get('quantity'):
            return render_template(
                "inventory/update.html",
                item=item,
                error="Nombre y cantidad son campos obligatorios"
            ), 400
            
        updated_item = inventory_service.update(item, data)
        flash(f"Ítem '{updated_item.name}' actualizado exitosamente!", 'success')
        return redirect(url_for('inventory.get_all_inventory'))
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
                "message": "Item not found"
            }), 404
            
        inventory_service.delete(item)
        return jsonify({
            "success": True,
            "message": "Item deleted",
            "deleted_id": item_id
        }), 200
    except SQLAlchemyError as e:
        return jsonify({
            "success": False,
            "message": "Database error"
        }), 500
    except Exception as e:
        return jsonify({
            "success": False,
            "message": "Server error"
        }), 500