# Portfolio Website - Windows XP Themed with Flask CMS

## Overview

This is a Windows XP-themed personal portfolio website built with Next.js for the frontend and Flask for the backend CMS. The project combines nostalgia with modern web technologies to create an interactive portfolio that mimics the classic Windows XP operating system interface.

The application serves a static Next.js frontend with a Windows XP UI, while providing a Flask-based content management system for updating portfolio projects, resume information, and web links through an admin panel.

## Quick Start

### Option 1: Direct Execution (Replit)

To run the application with a single command:

```bash
./start.sh
```

This script will:
1. Install Python dependencies (uv sync)
2. Install NPM packages (npm install)
3. Build the Next.js frontend (npm run build)
4. Initialize the database with all tables
5. Start the Flask backend on port 5000

### Option 2: Docker Deployment

For production or containerized environments:

```bash
# 1. Configure environment
cp .env.example .env
# Edit .env with your settings

# 2. Start with Docker Compose
docker-compose up --build -d

# 3. Initialize database
docker-compose exec web python backend/init_db.py
```

See [DOCKER.md](DOCKER.md) for complete Docker deployment guide.

**First Time Access:**
- Portfolio Website: Your Replit URL (or http://localhost:5000 for Docker)
- Admin Panel: `/admin/login`
  - Username: `admin`
  - Password: `admin123`
  - ⚠️ **IMPORTANT:** Change this password immediately after first login!

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture

**Technology Stack:**
- Next.js 15.4.5 configured for static export
- React 18.2.0 with Redux Toolkit for state management
- TypeScript for type safety
- Custom Windows XP-styled UI components

**Design Pattern:**
- Component-based architecture with reusable UI elements (WinForm, StartBar, DesktopIcon, etc.)
- Redux state management for window/tab handling and system settings
- Draggable and resizable windows using react-draggable and react-resizable
- Static site generation - Next.js exports to `out/` directory served by Flask

**Key Features:**
- Windows XP desktop environment simulation
- Draggable/resizable windows
- Start menu and taskbar functionality
- Multiple "applications" (My Work, Gallery, Outlook/Contact Form, Welcome)
- Image carousel for project galleries

### Backend Architecture

**Technology Stack:**
- Flask web framework with blueprints architecture
- Flask-SQLAlchemy ORM for database operations
- Flask-Login for session-based authentication
- Flask-Migrate for database migrations
- Flask-CORS for API endpoint protection

**Blueprint Structure:**
1. **API Blueprint** (`/api/*`) - Public REST endpoints for frontend data
2. **Admin Blueprint** (`/admin/*`) - Protected CMS interface and CRUD operations
3. **Frontend Blueprint** - Serves static Next.js build from `out/` directory

**Authentication:**
- Session-based authentication using Flask-Login
- Password hashing with Werkzeug security utilities
- Protected admin routes requiring login
- Login redirects for unauthorized access

**Data Models:**
- **User**: Admin authentication with hashed passwords
- **Project**: Portfolio projects with metadata, images, and ordering
- **ResumeInfo**: Resume/CV data storage
- **WebLink**: Social and professional links
- **SiteSettings**: Complete site personalization including PC name, owner name/email, social links (GitHub, LinkedIn), browser titles, about me content, and up to 4 profile images

### External Dependencies

**Database:**
- PostgreSQL as primary data store
- SQLAlchemy ORM for database abstraction
- Connection via DATABASE_URL environment variable

**Email Service:**
- Mailgun API for contact form submissions
- Configured via MAILGUN_API_KEY, FROM_EMAIL, and ADMIN_EMAIL environment variables
- Endpoint: `/api/send-email` (POST)

**Third-Party Libraries:**
- **xp.css** - Pre-styled Windows XP UI components
- **react-draggable** - Draggable window functionality
- **react-resizable** - Resizable window functionality
- **react-slick / slick-carousel** - Image carousel for galleries
- **axios** - HTTP client for API requests
- **uuid** - Unique ID generation for tabs/windows
- **Vercel Analytics** - Website analytics tracking

**Frontend API Integration:**
- Contact form sends to Next.js API route (`/api/send-email.ts`) which proxies to Mailgun
- Future integration points for dynamic content loading from Flask API endpoints

**Security:**
- CORS restricted to `/api/*` endpoints only
- CSRF protection enabled for admin forms
- SECRET_KEY environment variable for session signing
- File upload restrictions (images only, 16MB max)

**Admin Dashboard Features:**
- Site Personalization Settings (added November 2025):
  - PC name customization (appears in Start Menu)
  - Owner name and email configuration
  - Welcome page and browser tab titles
  - Social media links (GitHub, LinkedIn)
  - About Me content with multiple text sections
  - Profile image management (up to 4 images with preview)
  - Images uploaded to `backend/app/static/uploads` and served via `/admin/uploads/<filename>`
  - All settings accessible via `/api/site-settings` for frontend integration

**Deployment Considerations:**
- Static frontend served from Flask eliminates need for separate Next.js server
- Environment variables: DATABASE_URL (required), SECRET_KEY (auto-generated if not set), MAILGUN_API_KEY, ADMIN_EMAIL
- Upload folder: `backend/app/static/uploads` for user-uploaded images
- Default admin credentials: username `admin`, password `admin123` (change after first login!)