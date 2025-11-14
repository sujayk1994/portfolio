from app import create_app, db
from app.models import User
from dotenv import load_dotenv
import os

load_dotenv()

app = create_app()

@app.cli.command()
def init_db():
    """Initialize the database and create admin user."""
    db.create_all()
    
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(username='admin', email='admin@example.com')
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print('Database initialized! Admin user created.')
        print('Username: admin')
        print('Password: admin123')
        print('IMPORTANT: Change the password after first login!')
    else:
        print('Admin user already exists.')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port, debug=True)
