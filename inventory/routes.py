from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models import InventoryUpload

inventory = Blueprint('inventory', __name__)

@inventory.route('/history')
@login_required
def history():
    # Get all uploads for the current user, ordered by upload time
    uploads = InventoryUpload.query.filter_by(user_id=current_user.id).order_by(InventoryUpload.upload_time.desc()).all()
    
    return render_template('inventory/history.html', uploads=uploads)
