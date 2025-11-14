# Portfolio Website - Flask CMS Migration

This is a Windows XP-themed portfolio website that has been converted from Next.js to Flask with a content management system (CMS).

## 🎯 What's Been Done

### ✅ Completed
1. **Flask Backend Setup**
   - Flask application structure with blueprints (API, Admin, Frontend)
   - PostgreSQL database integration
   - Flask-Login authentication system
   - Flask-SQLAlchemy ORM with models

2. **Database Models**
   - User model with secure password hashing
   - Project model for portfolio projects
   - ResumeInfo model for resume data
   - WebLink model for social/professional links

3. **API Endpoints** (`/api/*`)
   - `GET /api/projects` - List all active projects
   - `GET /api/projects/<id>` - Get single project
   - `GET /api/resume` - Get resume information
   - `GET /api/links` - Get all active links
   - `POST /api/send-email` - Contact form submission

4. **Admin Panel** (`/admin/*`)
   - Login page at `/admin/login`
   - Dashboard at `/admin/dashboard` (requires login)
   - CRUD API endpoints for managing content
   - Basic templates created

5. **Frontend**
   - Next.js app configured for static export
   - Windows XP UI preserved exactly as before
   - Static files served by Flask from the `out/` directory

6. **Security Improvements**
   - SECRET_KEY environment variable required
   - Password hashing with Werkzeug
   - CORS restricted to API endpoints only
   - Session-based authentication

## 🚀 Getting Started

### Access the Application

**Portfolio Website:** Your main Replit URL

**Admin Panel:** `/admin/login`
- Username: `admin`
- Password: `admin123`
- **⚠️ IMPORTANT: Change this password immediately!**

### Environment Setup

The application uses environment variables stored in `backend/.env`:
- `SECRET_KEY` - Flask secret key for sessions (already generated)
- `DATABASE_URL` - PostgreSQL connection string (auto-configured by Replit)

## 📝 What Still Needs to Be Done

### 🔴 Critical (Security & Functionality)

1. **Change Default Admin Password** - Current credentials are insecure
2. **Complete Admin Dashboard JavaScript** - Forms need to be wired to API
3. **Add CSRF Protection** - Flask-WTF for all state-changing operations
4. **Implement File Upload System** - For project images and resume PDF
5. **Add API Input Validation** - Validate and sanitize all inputs
6. **Add Rate Limiting** - Especially for login and contact form

### 🟡 Important (Features)

7. **Update React Components** - Fetch data from Flask API instead of static
8. **Configure Email Service** - Mailgun, SendGrid, or similar
9. **Database Migrations** - Use Flask-Migrate properly
10. **Admin Features** - User management, logging, export

### 🟢 Nice to Have

11. Rich text editor for descriptions
12. Image optimization
13. Backup/restore functionality
14. Analytics dashboard

## 🏗️ Project Structure

```
├── backend/
│   ├── app/
│   │   ├── __init__.py          # Flask app factory
│   │   ├── models.py             # Database models
│   │   ├── routes/
│   │   │   ├── api.py            # Public API endpoints
│   │   │   ├── admin.py          # Admin panel endpoints
│   │   │   └── frontend.py       # Serve React frontend
│   │   └── templates/
│   │       └── admin/            # Admin panel templates
│   ├── app.py                    # Application entry point
│   ├── init_db.py                # Database initialization
│   └── .env                      # Environment variables (DO NOT COMMIT)
├── src/                          # Next.js/React source
├── out/                          # Static export (served by Flask)
└── package.json                  # Node dependencies
```

## 🛠️ Development

### Initialize Database
```bash
cd backend
python init_db.py
```

### Rebuild Frontend
```bash
npm run build
```

## ⚠️ Known Issues

1. **React Console Errors:** Static export has hydration warnings
2. **Admin Dashboard:** UI created but JavaScript not wired up yet
3. **File Uploads:** Not yet implemented
4. **CSRF Protection:** Not yet implemented

## 🔐 Security Checklist

Before going live:
- [ ] Change default admin credentials
- [ ] Implement CSRF protection
- [ ] Add rate limiting
- [ ] Validate all inputs
- [ ] Implement file upload security
- [ ] Use HTTPS only
- [ ] Review CORS settings

---

**Status:** ⚠️ Core functionality complete, admin panel needs JavaScript implementation
