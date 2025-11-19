from flask import Blueprint, jsonify, request, render_template, redirect, url_for, current_app, send_from_directory
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User, Project, ResumeInfo, WebLink, SiteSettings, Folder, DesignWork
from werkzeug.utils import secure_filename
from PIL import Image
import os
import uuid

bp = Blueprint('admin', __name__, url_prefix='/admin')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/login', methods=['GET'])
def login_page():
    return render_template('admin/login.html')

@bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('admin/visual_dashboard.html')

@bp.route('/dashboard/old')
@login_required
def old_dashboard():
    return render_template('admin/dashboard.html')

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    user = User.query.filter_by(username=username).first()
    
    if user and user.check_password(password):
        login_user(user)
        return jsonify({'message': 'Logged in successfully', 'user': {'username': user.username, 'email': user.email}}), 200
    
    return jsonify({'message': 'Invalid credentials'}), 401

@bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'}), 200

@bp.route('/projects', methods=['POST'])
@login_required
def create_project():
    data = request.get_json()
    
    project = Project(
        title=data.get('title'),
        description=data.get('description'),
        technologies=data.get('technologies'),
        github_url=data.get('github_url'),
        live_url=data.get('live_url'),
        image_url=data.get('image_url'),
        display_order=data.get('display_order', 0),
        is_active=data.get('is_active', True)
    )
    
    db.session.add(project)
    db.session.commit()
    
    return jsonify(project.to_dict()), 201

@bp.route('/projects/<int:project_id>', methods=['PUT'])
@login_required
def update_project(project_id):
    project = Project.query.get_or_404(project_id)
    data = request.get_json()
    
    project.title = data.get('title', project.title)
    project.description = data.get('description', project.description)
    project.technologies = data.get('technologies', project.technologies)
    project.github_url = data.get('github_url', project.github_url)
    project.live_url = data.get('live_url', project.live_url)
    project.image_url = data.get('image_url', project.image_url)
    project.display_order = data.get('display_order', project.display_order)
    project.is_active = data.get('is_active', project.is_active)
    
    db.session.commit()
    
    return jsonify(project.to_dict())

@bp.route('/projects/<int:project_id>', methods=['DELETE'])
@login_required
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    
    return jsonify({'message': 'Project deleted'}), 200

@bp.route('/resume', methods=['PUT'])
@login_required
def update_resume():
    data = request.get_json()
    resume = ResumeInfo.query.first()
    
    if not resume:
        resume = ResumeInfo()
        db.session.add(resume)
    
    resume.full_name = data.get('full_name', resume.full_name)
    resume.title = data.get('title', resume.title)
    resume.email = data.get('email', resume.email)
    resume.phone = data.get('phone', resume.phone)
    resume.location = data.get('location', resume.location)
    resume.summary = data.get('summary', resume.summary)
    resume.skills = data.get('skills', resume.skills)
    resume.resume_pdf_url = data.get('resume_pdf_url', resume.resume_pdf_url)
    
    db.session.commit()
    
    return jsonify(resume.to_dict())

@bp.route('/links', methods=['POST'])
@login_required
def create_link():
    data = request.get_json()
    
    link = WebLink(
        title=data.get('title'),
        url=data.get('url'),
        icon=data.get('icon'),
        display_order=data.get('display_order', 0),
        is_active=data.get('is_active', True)
    )
    
    db.session.add(link)
    db.session.commit()
    
    return jsonify(link.to_dict()), 201

@bp.route('/links/<int:link_id>', methods=['PUT'])
@login_required
def update_link(link_id):
    link = WebLink.query.get_or_404(link_id)
    data = request.get_json()
    
    link.title = data.get('title', link.title)
    link.url = data.get('url', link.url)
    link.icon = data.get('icon', link.icon)
    link.display_order = data.get('display_order', link.display_order)
    link.is_active = data.get('is_active', link.is_active)
    
    db.session.commit()
    
    return jsonify(link.to_dict())

@bp.route('/links/<int:link_id>', methods=['DELETE'])
@login_required
def delete_link(link_id):
    link = WebLink.query.get_or_404(link_id)
    db.session.delete(link)
    db.session.commit()
    
    return jsonify({'message': 'Link deleted'}), 200

@bp.route('/settings', methods=['GET'])
@login_required
def get_settings():
    settings = SiteSettings.query.first()
    if not settings:
        settings = SiteSettings()
        db.session.add(settings)
        db.session.commit()
    return jsonify(settings.to_dict())

@bp.route('/settings', methods=['PUT'])
@login_required
def update_settings():
    data = request.get_json()
    settings = SiteSettings.query.first()
    
    if not settings:
        settings = SiteSettings()
        db.session.add(settings)
    
    settings.pc_name = data.get('pc_name', settings.pc_name)
    settings.welcome_title = data.get('welcome_title', settings.welcome_title)
    settings.browser_tab_title = data.get('browser_tab_title', settings.browser_tab_title)
    settings.owner_name = data.get('owner_name', settings.owner_name)
    settings.owner_email = data.get('owner_email', settings.owner_email)
    settings.github_url = data.get('github_url', settings.github_url)
    settings.linkedin_url = data.get('linkedin_url', settings.linkedin_url)
    settings.about_intro = data.get('about_intro', settings.about_intro)
    settings.about_why_site = data.get('about_why_site', settings.about_why_site)
    settings.about_interests = data.get('about_interests', settings.about_interests)
    settings.about_interests2 = data.get('about_interests2', settings.about_interests2)
    settings.about_interests3 = data.get('about_interests3', settings.about_interests3)
    settings.boot_screen_line1 = data.get('boot_screen_line1', settings.boot_screen_line1)
    settings.boot_screen_line2 = data.get('boot_screen_line2', settings.boot_screen_line2)
    settings.boot_screen_copyright = data.get('boot_screen_copyright', settings.boot_screen_copyright)
    
    db.session.commit()
    
    return jsonify(settings.to_dict())

@bp.route('/upload-image', methods=['POST'])
@login_required
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        ext = filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4().hex}.{ext}"
        
        upload_folder = current_app.config['UPLOAD_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)
        
        filepath = os.path.join(upload_folder, unique_filename)
        file.save(filepath)
        
        return jsonify({
            'filename': unique_filename,
            'url': f'/admin/uploads/{unique_filename}'
        }), 200
    
    return jsonify({'error': 'File type not allowed'}), 400

@bp.route('/update-profile-image', methods=['POST'])
@login_required
def update_profile_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    image_slot = request.form.get('slot', '1')
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        ext = filename.rsplit('.', 1)[1].lower()
        unique_filename = f"profile_{image_slot}_{uuid.uuid4().hex}.{ext}"
        
        upload_folder = current_app.config['UPLOAD_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)
        
        filepath = os.path.join(upload_folder, unique_filename)
        file.save(filepath)
        
        settings = SiteSettings.query.first()
        if not settings:
            settings = SiteSettings()
            db.session.add(settings)
        
        image_url = f'/admin/uploads/{unique_filename}'
        
        if image_slot == '1':
            settings.profile_image_1 = image_url
        elif image_slot == '2':
            settings.profile_image_2 = image_url
        elif image_slot == '3':
            settings.profile_image_3 = image_url
        elif image_slot == '4':
            settings.profile_image_4 = image_url
        
        db.session.commit()
        
        return jsonify({
            'filename': unique_filename,
            'url': image_url,
            'slot': image_slot
        }), 200
    
    return jsonify({'error': 'File type not allowed'}), 400

@bp.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

@bp.route('/settings-dashboard')
@login_required
def settings_dashboard():
    return render_template('admin/settings.html')

@bp.route('/folders', methods=['GET'])
@login_required
def get_folders():
    folders = Folder.query.order_by(Folder.display_order, Folder.created_at.desc()).all()
    return jsonify([folder.to_dict() for folder in folders])

@bp.route('/folders', methods=['POST'])
@login_required
def create_folder():
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Invalid JSON payload'}), 400
    
    if not data.get('name'):
        return jsonify({'error': 'name is required'}), 400
    
    folder = Folder(
        name=data.get('name'),
        description=data.get('description'),
        icon_type=data.get('icon_type', 'folder'),
        display_order=data.get('display_order', 0),
        is_active=data.get('is_active', True)
    )
    
    db.session.add(folder)
    db.session.commit()
    
    return jsonify(folder.to_dict()), 201

@bp.route('/folders/<int:folder_id>', methods=['PUT'])
@login_required
def update_folder(folder_id):
    folder = Folder.query.get_or_404(folder_id)
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Invalid JSON payload'}), 400
    
    folder.name = data.get('name', folder.name)
    folder.description = data.get('description', folder.description)
    folder.icon_type = data.get('icon_type', folder.icon_type)
    folder.display_order = data.get('display_order', folder.display_order)
    folder.is_active = data.get('is_active', folder.is_active)
    
    db.session.commit()
    
    return jsonify(folder.to_dict())

@bp.route('/folders/<int:folder_id>', methods=['DELETE'])
@login_required
def delete_folder(folder_id):
    folder = Folder.query.get_or_404(folder_id)
    db.session.delete(folder)
    db.session.commit()
    
    return jsonify({'message': 'Folder deleted'}), 200

@bp.route('/design-work', methods=['GET'])
@login_required
def get_design_work():
    folder_id = request.args.get('folder_id', type=int)
    
    if folder_id:
        items = DesignWork.query.filter_by(folder_id=folder_id).order_by(DesignWork.display_order, DesignWork.created_at.desc()).all()
    else:
        items = DesignWork.query.order_by(DesignWork.display_order, DesignWork.created_at.desc()).all()
    
    return jsonify([item.to_dict() for item in items])

@bp.route('/design-work', methods=['POST'])
@login_required
def create_design_work():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    folder_id = request.form.get('folder_id')
    title = request.form.get('title')
    description = request.form.get('description', '')
    client_name = request.form.get('client_name', '')
    tags = request.form.get('tags', '')
    display_order = request.form.get('display_order', 0, type=int)
    project_date = request.form.get('project_date')
    is_active = request.form.get('is_active', 'true').lower() == 'true'
    
    if not folder_id:
        return jsonify({'error': 'folder_id is required'}), 400
    
    try:
        folder_id_int = int(folder_id)
    except (ValueError, TypeError):
        return jsonify({'error': 'folder_id must be a valid integer'}), 400
    
    folder = Folder.query.get(folder_id_int)
    if not folder:
        return jsonify({'error': 'Folder not found'}), 404
    
    if not title:
        return jsonify({'error': 'title is required'}), 400
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        ext = filename.rsplit('.', 1)[1].lower()
        unique_filename = f"design_{uuid.uuid4().hex}.{ext}"
        
        upload_folder = current_app.config['UPLOAD_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)
        
        filepath = os.path.join(upload_folder, unique_filename)
        file.save(filepath)
        
        file_size = os.path.getsize(filepath)
        width, height = None, None
        
        try:
            with Image.open(filepath) as img:
                width, height = img.size
                
                thumbnail_filename = f"thumb_{unique_filename}"
                thumbnail_path = os.path.join(upload_folder, thumbnail_filename)
                img.thumbnail((200, 200))
                img.save(thumbnail_path)
                thumbnail_url = f'/admin/uploads/{thumbnail_filename}'
        except Exception as e:
            thumbnail_url = None
        
        from datetime import datetime as dt
        parsed_date = None
        if project_date:
            try:
                parsed_date = dt.fromisoformat(project_date.replace('Z', '+00:00')).date()
            except:
                pass
        
        design_work = DesignWork(
            title=title,
            description=description,
            file_url=f'/admin/uploads/{unique_filename}',
            thumbnail_url=thumbnail_url,
            file_type=ext,
            file_size=file_size,
            width=width,
            height=height,
            client_name=client_name,
            project_date=parsed_date,
            tags=tags,
            display_order=display_order,
            is_active=is_active,
            folder_id=folder_id_int
        )
        
        db.session.add(design_work)
        db.session.commit()
        
        return jsonify(design_work.to_dict()), 201
    
    return jsonify({'error': 'File type not allowed'}), 400

@bp.route('/design-work/<int:work_id>', methods=['PUT'])
@login_required
def update_design_work(work_id):
    work = DesignWork.query.get_or_404(work_id)
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Invalid JSON payload'}), 400
    
    if 'folder_id' in data:
        try:
            new_folder_id = int(data['folder_id'])
        except (ValueError, TypeError):
            return jsonify({'error': 'folder_id must be a valid integer'}), 400
        
        folder = Folder.query.get(new_folder_id)
        if not folder:
            return jsonify({'error': 'Folder not found'}), 404
        
        work.folder_id = new_folder_id
    
    work.title = data.get('title', work.title)
    work.description = data.get('description', work.description)
    work.client_name = data.get('client_name', work.client_name)
    work.tags = data.get('tags', work.tags)
    work.display_order = data.get('display_order', work.display_order)
    work.is_active = data.get('is_active', work.is_active)
    
    if 'project_date' in data:
        from datetime import datetime as dt
        project_date = data['project_date']
        if project_date:
            try:
                work.project_date = dt.fromisoformat(project_date.replace('Z', '+00:00')).date()
            except:
                return jsonify({'error': 'Invalid project_date format'}), 400
        else:
            work.project_date = None
    
    db.session.commit()
    
    return jsonify(work.to_dict())

@bp.route('/design-work/<int:work_id>', methods=['DELETE'])
@login_required
def delete_design_work(work_id):
    work = DesignWork.query.get_or_404(work_id)
    db.session.delete(work)
    db.session.commit()
    
    return jsonify({'message': 'Design work deleted'}), 200
