# Docker Deployment Guide

This guide explains how to run your Windows XP Portfolio website using Docker and Docker Compose.

## 📋 Prerequisites

- Docker Engine 20.10+ ([Install Docker](https://docs.docker.com/get-docker/))
- Docker Compose 2.0+ ([Install Docker Compose](https://docs.docker.com/compose/install/))
- At least 2GB of available disk space
- At least 1GB of available RAM

## 🚀 Quick Start

### 1. Configure Environment Variables

Copy the example environment file and configure it:

```bash
cp .env.example .env
```

Edit `.env` and set your values:

```env
# Database Configuration
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your-secure-password-here
POSTGRES_DB=portfolio_db

# Application Configuration
SECRET_KEY=generate-a-secure-secret-key-here
```

**Generate a secure SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 2. Build and Start the Application

Build and start all services:

```bash
docker-compose up --build -d
```

This will:
- Build the Next.js frontend
- Build the Flask backend
- Start PostgreSQL database
- Initialize database tables
- Start the application on port 5000

### 3. Initialize Database

Run the database initialization script:

```bash
docker-compose exec web python backend/init_db.py
```

This creates:
- All required database tables
- Admin user (username: `admin`, password: `admin123`)

### 4. Access Your Application

- **Portfolio Website:** http://localhost:5000
- **Admin Panel:** http://localhost:5000/admin/login
  - Username: `admin`
  - Password: `admin123`
  - ⚠️ **IMPORTANT:** Change this password immediately after first login!

## 🛠️ Docker Commands

### View Running Containers

```bash
docker-compose ps
```

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f web
docker-compose logs -f database
```

### Stop Services

```bash
# Stop all services
docker-compose stop

# Stop and remove containers
docker-compose down

# Stop, remove containers, and delete volumes (⚠️ deletes database!)
docker-compose down -v
```

### Restart Services

```bash
# Restart all services
docker-compose restart

# Restart specific service
docker-compose restart web
```

### Access Container Shell

```bash
# Access web container
docker-compose exec web /bin/sh

# Access database
docker-compose exec database psql -U postgres -d portfolio_db
```

### Rebuild After Code Changes

```bash
# Rebuild and restart
docker-compose up --build -d

# Force rebuild without cache
docker-compose build --no-cache
docker-compose up -d
```

## 🗄️ Database Management

### Backup Database

```bash
docker-compose exec database pg_dump -U postgres portfolio_db > backup.sql
```

### Restore Database

```bash
cat backup.sql | docker-compose exec -T database psql -U postgres portfolio_db
```

### View Database

```bash
docker-compose exec database psql -U postgres -d portfolio_db
```

Inside psql:
```sql
-- List all tables
\dt

-- View users
SELECT * FROM users;

-- View projects
SELECT * FROM projects;

-- Exit
\q
```

## 🔧 Troubleshooting

### Port Already in Use

If port 5000 or 5432 is already in use, change it in `.env`:

```env
APP_PORT=8000
POSTGRES_PORT=5433
```

Then access at http://localhost:8000

### Database Connection Issues

Check if database is healthy:

```bash
docker-compose exec database pg_isready -U postgres
```

### Permission Errors

If you encounter permission errors with uploads:

```bash
docker-compose exec web mkdir -p backend/app/static/uploads
docker-compose exec web chmod 777 backend/app/static/uploads
```

### View Application Errors

```bash
docker-compose logs -f web | grep ERROR
```

### Reset Everything

```bash
# Stop and remove everything
docker-compose down -v

# Remove images
docker rmi $(docker images -q portfolio*)

# Start fresh
docker-compose up --build -d
```

## 📊 Performance Tuning

### Adjust Gunicorn Workers

In `.env`, set based on your server resources:

```env
# Formula: (2 × CPU_CORES) + 1
GUNICORN_WORKERS=4

# Threads per worker (2-4 recommended)
GUNICORN_THREADS=2
```

### Memory Limits

Add to `docker-compose.yml` under the `web` service:

```yaml
web:
  # ... existing config ...
  deploy:
    resources:
      limits:
        memory: 512M
      reservations:
        memory: 256M
```

## 🔒 Production Deployment

### Security Checklist

- [ ] Set strong `SECRET_KEY` in `.env`
- [ ] Change default admin password
- [ ] Set strong database password
- [ ] Configure firewall rules (only expose port 80/443)
- [ ] Use environment-specific `.env` files
- [ ] Enable HTTPS (use Nginx reverse proxy + Let's Encrypt)
- [ ] Regular database backups
- [ ] Monitor logs for suspicious activity

### Using with Nginx Reverse Proxy

Create `nginx.conf`:

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    client_max_body_size 16M;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Environment Variables for Production

Create `.env.production`:

```env
FLASK_ENV=production
SECRET_KEY=your-production-secret-key
POSTGRES_PASSWORD=strong-production-password
LOG_LEVEL=warning
```

Use it:

```bash
docker-compose --env-file .env.production up -d
```

## 📁 Project Structure

```
.
├── Dockerfile                 # Multi-stage build for production
├── docker-compose.yml         # Docker Compose configuration
├── gunicorn_config.py         # Gunicorn server configuration
├── .env                       # Environment variables (not committed)
├── .env.example               # Example environment file
├── backend/                   # Flask application
│   ├── app/                   # Flask app code
│   ├── app.py                 # Main application file
│   └── init_db.py             # Database initialization
├── src/                       # Next.js source files
├── out/                       # Next.js build output (in container)
└── DOCKER.md                  # This file
```

## 🔄 Updates and Maintenance

### Update Application Code

1. Pull latest code
2. Rebuild containers:

```bash
git pull
docker-compose up --build -d
```

### Database Migrations

If you add new models or change the database schema:

```bash
# Access container
docker-compose exec web /bin/sh

# Run migration script or update schema
python backend/init_db.py
```

## 📝 Health Checks

The application includes built-in health checks:

- **Application health:** http://localhost:5000/api/projects
- **Database health:** Automatically checked by Docker Compose

Check health status:

```bash
docker-compose ps
```

Healthy services show `(healthy)` in the status.

## 🆘 Getting Help

If you encounter issues:

1. Check logs: `docker-compose logs -f`
2. Verify environment variables: `docker-compose config`
3. Check service status: `docker-compose ps`
4. Review this documentation
5. Check Docker and Docker Compose versions

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Flask Deployment](https://flask.palletsprojects.com/en/stable/deploying/)
- [Gunicorn Documentation](https://docs.gunicorn.org/)
- [PostgreSQL Docker Image](https://hub.docker.com/_/postgres)

---

**Note:** This Docker setup is production-ready with security best practices, health checks, and optimized builds. For development, use `./start.sh` instead.
