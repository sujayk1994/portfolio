from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    db.create_all()
    
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(username='admin', email='admin@portfolio.com')
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print('\n=== Database Initialized Successfully! ===')
        print('Admin user created:')
        print('  Username: admin')
        print('  Password: admin123')
        print('\nIMPORTANT: Change the password after first login!')
        print('Access the admin panel at: /admin/login')
    else:
        print('Admin user already exists.')
