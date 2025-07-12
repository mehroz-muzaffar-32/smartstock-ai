from flask import current_app
from flask_sqlalchemy import SQLAlchemy

def upgrade():
    with current_app.app_context():
        db = SQLAlchemy()
        
        # Create InventoryUpload table
        db.engine.execute('''
            CREATE TABLE IF NOT EXISTS inventory_upload (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                filename VARCHAR(255) NOT NULL,
                upload_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES user (id)
            )
        ''')
        
        # Create InventoryItem table
        db.engine.execute('''
            CREATE TABLE IF NOT EXISTS inventory_item (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                upload_id INTEGER NOT NULL,
                name VARCHAR(255) NOT NULL,
                quantity INTEGER NOT NULL,
                FOREIGN KEY (upload_id) REFERENCES inventory_upload (id)
            )
        ''')
        
        # Create indexes
        db.engine.execute('CREATE INDEX IF NOT EXISTS idx_upload_user ON inventory_upload (user_id)')
        db.engine.execute('CREATE INDEX IF NOT EXISTS idx_item_upload ON inventory_item (upload_id)')
        
        # Commit changes
        db.session.commit()

def downgrade():
    with current_app.app_context():
        db = SQLAlchemy()
        
        # Drop tables
        db.engine.execute('DROP TABLE IF EXISTS inventory_item')
        db.engine.execute('DROP TABLE IF EXISTS inventory_upload')
        
        # Commit changes
        db.session.commit()
