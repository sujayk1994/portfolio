from flask import Blueprint, jsonify, request
from app import db
from app.models import Project, ResumeInfo, WebLink, SiteSettings, Folder, DesignWork
from flask_login import login_required

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
        'profile_image_4': None
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
