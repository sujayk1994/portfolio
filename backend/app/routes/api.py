from flask import Blueprint, jsonify, request
from app import db
from app.models import Project, ResumeInfo, WebLink, SiteSettings, Folder, DesignWork
from flask_login import login_required
from datetime import datetime

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/projects', methods=['GET'])
def get_projects():
    projects = Project.query.filter_by(is_active=True).order_by(Project.display_order).all()
    return jsonify([p.to_dict() for p in projects])

@bp.route('/projects/<int:project_id>', methods=['GET'])
def get_project(project_id):
    project = Project.query.get_or_404(project_id)
    return jsonify(project.to_dict())

@bp.route('/resume', methods=['GET'])
def get_resume():
    resume = ResumeInfo.query.first()
    if resume:
        return jsonify(resume.to_dict())
    return jsonify({'message': 'Resume info not found'}), 404

@bp.route('/links', methods=['GET'])
def get_links():
    links = WebLink.query.filter_by(is_active=True).order_by(WebLink.display_order).all()
    return jsonify([link.to_dict() for link in links])

@bp.route('/send-email', methods=['POST'])
def send_email():
    data = request.get_json()
    
    from_email = data.get('from')
    subject = data.get('subject')
    message = data.get('message')
    
    if not all([from_email, subject, message]):
        return jsonify({'message': 'Missing required fields'}), 400
    
    return jsonify({'message': 'Email sent successfully'}), 200

@bp.route('/site-settings', methods=['GET'])
def get_site_settings():
    settings = SiteSettings.query.first()
    if settings:
        return jsonify(settings.to_dict())
    return jsonify({
        'pc_name': "Sujay K's PC",
        'welcome_title': "Welcome To Sujay K's Personal Website",
        'browser_tab_title': "Sujay K's Personal Website - Home Page",
        'owner_name': "Sujay K",
        'owner_email': "your-email@example.com",
        'github_url': "https://github.com/yourusername",
        'linkedin_url': "https://linkedin.com/in/yourusername",
        'about_intro': "Hi, I'm Sujay K, an aspiring software engineer and entrepreneur...",
        'about_why_site': '',
        'about_interests': '',
        'about_interests2': '',
        'about_interests3': '',
        'profile_image_1': None,
        'profile_image_2': None,
        'profile_image_3': None,
        'profile_image_4': None,
        'boot_screen_line1': "Sujay's",
        'boot_screen_line2': "Portfolio",
        'boot_screen_copyright': "Copyright © Sujay K"
    })

@bp.route('/folders', methods=['GET'])
def get_public_folders():
    folders = Folder.query.filter_by(is_active=True).order_by(Folder.display_order, Folder.created_at.desc()).all()
    return jsonify([folder.to_dict() for folder in folders])

@bp.route('/folders/<int:folder_id>', methods=['GET'])
def get_folder_details(folder_id):
    folder = Folder.query.get_or_404(folder_id)
    if not folder.is_active:
        return jsonify({'message': 'Folder not found'}), 404
    return jsonify(folder.to_dict())

@bp.route('/folders/<int:folder_id>/work', methods=['GET'])
def get_folder_work(folder_id):
    folder = Folder.query.get_or_404(folder_id)
    if not folder.is_active:
        return jsonify({'message': 'Folder not found'}), 404
    
    items = DesignWork.query.filter_by(folder_id=folder_id, is_active=True).order_by(DesignWork.display_order, DesignWork.created_at.desc()).all()
    return jsonify([item.to_dict() for item in items])

# Admin endpoints for folder management
@bp.route('/folders', methods=['POST'])
@login_required
def create_folder():
    data = request.get_json()
    folder = Folder(
        name=data.get('name'),
        description=data.get('description'),
        display_order=Folder.query.count()
    )
    db.session.add(folder)
    db.session.commit()
    return jsonify(folder.to_dict()), 201

@bp.route('/folders/<int:folder_id>', methods=['DELETE'])
@login_required
def delete_folder(folder_id):
    folder = Folder.query.get_or_404(folder_id)
    db.session.delete(folder)
    db.session.commit()
    return jsonify({'message': 'Folder deleted'}), 200

@bp.route('/folders/<int:folder_id>/items', methods=['GET'])
@login_required
def get_folder_items(folder_id):
    items = DesignWork.query.filter_by(folder_id=folder_id).order_by(DesignWork.display_order, DesignWork.created_at.desc()).all()
    return jsonify([item.to_dict() for item in items])

@bp.route('/folders/<int:folder_id>/upload', methods=['POST'])
@login_required
def upload_to_folder(folder_id):
    from werkzeug.utils import secure_filename
    import os
    from PIL import Image
    
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
    folder = Folder.query.get_or_404(folder_id)
    
    if 'files' not in request.files:
        return jsonify({'message': 'No files provided'}), 400
    
    files = request.files.getlist('files')
    uploaded_items = []
    
    upload_dir = 'backend/app/static/uploads'
    os.makedirs(upload_dir, exist_ok=True)
    
    for file in files:
        if file and file.filename:
            if not allowed_file(file.filename):
                continue
            
            filename = secure_filename(file.filename)
            timestamp = int(datetime.now().timestamp())
            unique_filename = f"{timestamp}_{filename}"
            filepath = os.path.join(upload_dir, unique_filename)
            
            file.save(filepath)
            
            # Get image dimensions
            try:
                with Image.open(filepath) as img:
                    width, height = img.size
            except:
                width, height = None, None
            
            # Create database entry
            design_item = DesignWork(
                title=filename,
                file_url=f'/static/uploads/{unique_filename}',
                thumbnail_url=f'/static/uploads/{unique_filename}',
                file_type=file.content_type,
                file_size=os.path.getsize(filepath),
                width=width,
                height=height,
                folder_id=folder_id,
                display_order=DesignWork.query.filter_by(folder_id=folder_id).count()
            )
            db.session.add(design_item)
            uploaded_items.append(design_item)
    
    db.session.commit()
    return jsonify([item.to_dict() for item in uploaded_items]), 201

@bp.route('/design-work/<int:item_id>', methods=['DELETE'])
@login_required
def delete_design_item(item_id):
    item = DesignWork.query.get_or_404(item_id)
    
    # Delete file from disk
    import os
    if item.file_url:
        file_path = item.file_url.replace('/static/uploads/', 'backend/app/static/uploads/')
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass
    
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Item deleted'}), 200

@bp.route('/site-settings/<int:settings_id>', methods=['PUT'])
@login_required
def update_site_settings(settings_id):
    settings = SiteSettings.query.get_or_404(settings_id)
    data = request.get_json()
    
    for key, value in data.items():
        if hasattr(settings, key):
            setattr(settings, key, value)
    
    db.session.commit()
    return jsonify(settings.to_dict()), 200
