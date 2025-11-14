from app import create_app, db
from app.models import User
from sqlalchemy import inspect

app = create_app()

with app.app_context():
    inspector = inspect(db.engine)
    existing_tables = inspector.get_table_names()
    
    if not existing_tables:
        print('\n=== First-time setup: Creating database tables ===')
        print('Note: Use migrations for future schema changes')
        db.create_all()
    else:
        print('\n=== Database tables already exist ===')
        print('Skipping db.create_all() - use migrations for schema updates')
    
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(username='admin', email='admin@portfolio.com')
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print('\n=== Admin user created ===')
        print('  Username: admin')
        print('  Password: admin123')
        print('\nIMPORTANT: Change the password after first login!')
        print('Access the admin panel at: /admin/login')
    else:
        print('Admin user already exists.')
