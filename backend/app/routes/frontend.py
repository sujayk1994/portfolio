from flask import Blueprint, send_from_directory, current_app
import os

bp = Blueprint('frontend', __name__)

@bp.route('/')
def index():
    out_dir = os.path.join(current_app.root_path, '../../out')
    if os.path.exists(os.path.join(out_dir, 'index.html')):
        return send_from_directory(out_dir, 'index.html')
    else:
        return "<h1>Portfolio Site</h1><p>Frontend not built yet. Run 'npm run build' in the Next.js project to build the frontend.</p>"

@bp.route('/<path:path>')
def serve_static(path):
    out_dir = os.path.join(current_app.root_path, '../../out')
    if os.path.exists(os.path.join(out_dir, path)):
        return send_from_directory(out_dir, path)
    return send_from_directory(out_dir, 'index.html')
