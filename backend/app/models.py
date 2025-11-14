from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Project(db.Model):
    __tablename__ = 'projects'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    technologies = db.Column(db.Text)
    github_url = db.Column(db.String(500))
    live_url = db.Column(db.String(500))
    image_url = db.Column(db.String(500))
    display_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'technologies': self.technologies,
            'github_url': self.github_url,
            'live_url': self.live_url,
            'image_url': self.image_url,
            'display_order': self.display_order,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_active': self.is_active
        }

class ResumeInfo(db.Model):
    __tablename__ = 'resume_info'
    
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100))
    title = db.Column(db.String(200))
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    location = db.Column(db.String(100))
    summary = db.Column(db.Text)
    skills = db.Column(db.Text)
    resume_pdf_url = db.Column(db.String(500))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'title': self.title,
            'email': self.email,
            'phone': self.phone,
            'location': self.location,
            'summary': self.summary,
            'skills': self.skills,
            'resume_pdf_url': self.resume_pdf_url,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class WebLink(db.Model):
    __tablename__ = 'web_links'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    icon = db.Column(db.String(100))
    display_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'url': self.url,
            'icon': self.icon,
            'display_order': self.display_order,
            'is_active': self.is_active
        }

class SiteSettings(db.Model):
    __tablename__ = 'site_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    pc_name = db.Column(db.String(200), default="Sujay K's PC")
    welcome_title = db.Column(db.String(200), default="Welcome To Sujay K's Personal Website")
    browser_tab_title = db.Column(db.String(200), default="Sujay K's Personal Website - Home Page")
    owner_name = db.Column(db.String(100), default="Sujay K")
    owner_email = db.Column(db.String(120), default="your-email@example.com")
    github_url = db.Column(db.String(500), default="https://github.com/yourusername")
    linkedin_url = db.Column(db.String(500), default="https://linkedin.com/in/yourusername")
    about_intro = db.Column(db.Text, default="Hi, I'm Sujay K, an aspiring software engineer and entrepreneur...")
    about_why_site = db.Column(db.Text, default="I always love challenging myself to creating something different...")
    about_interests = db.Column(db.Text)
    about_interests2 = db.Column(db.Text)
    about_interests3 = db.Column(db.Text)
    profile_image_1 = db.Column(db.String(500))
    profile_image_2 = db.Column(db.String(500))
    profile_image_3 = db.Column(db.String(500))
    profile_image_4 = db.Column(db.String(500))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'pc_name': self.pc_name,
            'welcome_title': self.welcome_title,
            'browser_tab_title': self.browser_tab_title,
            'owner_name': self.owner_name,
            'owner_email': self.owner_email,
            'github_url': self.github_url,
            'linkedin_url': self.linkedin_url,
            'about_intro': self.about_intro,
            'about_why_site': self.about_why_site,
            'about_interests': self.about_interests,
            'about_interests2': self.about_interests2,
            'about_interests3': self.about_interests3,
            'profile_image_1': self.profile_image_1,
            'profile_image_2': self.profile_image_2,
            'profile_image_3': self.profile_image_3,
            'profile_image_4': self.profile_image_4,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Folder(db.Model):
    __tablename__ = 'folders'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    icon_type = db.Column(db.String(50), default='folder')
    display_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    design_items = db.relationship('DesignWork', backref='folder', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'icon_type': self.icon_type,
            'display_order': self.display_order,
            'is_active': self.is_active,
            'item_count': len([item for item in self.design_items if item.is_active]),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class DesignWork(db.Model):
    __tablename__ = 'design_work'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    file_url = db.Column(db.String(500), nullable=False)
    thumbnail_url = db.Column(db.String(500))
    file_type = db.Column(db.String(50))
    file_size = db.Column(db.Integer)
    width = db.Column(db.Integer)
    height = db.Column(db.Integer)
    client_name = db.Column(db.String(200))
    project_date = db.Column(db.Date)
    tags = db.Column(db.Text)
    display_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    folder_id = db.Column(db.Integer, db.ForeignKey('folders.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'file_url': self.file_url,
            'thumbnail_url': self.thumbnail_url,
            'file_type': self.file_type,
            'file_size': self.file_size,
            'width': self.width,
            'height': self.height,
            'client_name': self.client_name,
            'project_date': self.project_date.isoformat() if self.project_date else None,
            'tags': self.tags,
            'display_order': self.display_order,
            'is_active': self.is_active,
            'folder_id': self.folder_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
