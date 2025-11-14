# Admin Panel Guide - Editable Content

This guide details all the content you can edit through the admin panel.

## 🔐 Admin Access

**Login URL:** `/admin/login`

**Default Credentials:**
- Username: `admin`
- Password: `admin123`

⚠️ **IMPORTANT:** Change the password immediately after first login!

---

## ✅ What You Can Edit

### 1. **About Me Section** (Site Settings)

**Endpoint:** `/admin/settings`

Editable fields:
- **About Intro** - Your main introduction paragraph
- **Why This Site** - Explanation of why you created this site
- **Interests** - Your hobbies and interests (Section 1)
- **Interests 2** - Additional interests (Section 2)
- **Interests 3** - More interests (Section 3)
- **Profile Images** - Upload up to 4 profile pictures

**API Access:** 
- GET `/api/site-settings` - Public access to view settings
- PUT `/admin/settings` - Update settings (requires login)

---

### 2. **Resume Information**

**Endpoint:** `/admin/resume`

Editable fields:
- **Full Name** - Your complete name
- **Title** - Your professional title (e.g., "Software Engineer")
- **Email** - Contact email
- **Phone** - Phone number
- **Location** - Your city/location
- **Summary** - Professional summary or bio
- **Skills** - Your technical skills (comma-separated or formatted)
- **Resume PDF URL** - Link to downloadable PDF resume

**API Access:**
- GET `/api/resume` - Public access to view resume
- PUT `/admin/resume` - Update resume (requires login)

---

### 3. **Portfolio Projects**

**Endpoint:** `/admin/projects`

**Operations:**
- ✅ Create new projects (POST `/admin/projects`)
- ✅ Update existing projects (PUT `/admin/projects/<id>`)
- ✅ Delete projects (DELETE `/admin/projects/<id>`)

Editable fields per project:
- **Title** - Project name
- **Description** - Detailed description
- **Technologies** - Tech stack used
- **GitHub URL** - Link to GitHub repository
- **Live URL** - Link to live demo
- **Image URL** - Project screenshot/image
- **Display Order** - Order in which projects appear
- **Is Active** - Show/hide project

**API Access:**
- GET `/api/projects` - Public list of active projects
- GET `/api/projects/<id>` - View single project

---

### 4. **Web Links** (Social/Professional)

**Endpoint:** `/admin/links`

**Operations:**
- ✅ Create new links (POST `/admin/links`)
- ✅ Update links (PUT `/admin/links/<id>`)
- ✅ Delete links (DELETE `/admin/links/<id>`)

Editable fields per link:
- **Title** - Link display name
- **URL** - Link destination
- **Icon** - Icon identifier
- **Display Order** - Order of appearance
- **Is Active** - Show/hide link

**API Access:**
- GET `/api/links` - Public list of active links

---

### 5. **Design Work & Folders**

**Endpoints:** 
- `/admin/folders` - Manage folders
- `/admin/design-work` - Manage design items

#### Folders (Categories)

**Operations:**
- ✅ Create folders (POST `/admin/folders`)
- ✅ Update folders (PUT `/admin/folders/<id>`)
- ✅ Delete folders (DELETE `/admin/folders/<id>`)

Editable fields:
- **Name** - Folder name
- **Description** - Folder description
- **Icon Type** - Icon style
- **Display Order** - Sorting order
- **Is Active** - Show/hide folder

#### Design Work (Portfolio Items)

**Operations:**
- ✅ Upload design work (POST `/admin/design-work`)
- ✅ Update design work (PUT `/admin/design-work/<id>`)
- ✅ Delete design work (DELETE `/admin/design-work/<id>`)

Editable fields:
- **Title** - Design item title
- **Description** - Item description
- **File Upload** - Upload image/design file
- **Client Name** - Client or project name
- **Project Date** - Completion date
- **Tags** - Comma-separated tags
- **Display Order** - Sorting order
- **Is Active** - Show/hide item
- **Folder ID** - Assign to folder/category

**API Access:**
- GET `/api/folders` - Public list of folders
- GET `/api/folders/<id>/work` - Get work items in folder

---

### 6. **Site Personalization**

**Endpoint:** `/admin/settings`

Global site settings:
- **PC Name** - Computer name shown in Start Menu
- **Welcome Title** - Main welcome message
- **Browser Tab Title** - Title shown in browser tab
- **Owner Name** - Your name
- **Owner Email** - Contact email
- **GitHub URL** - Your GitHub profile
- **LinkedIn URL** - Your LinkedIn profile
- **Profile Images (1-4)** - Multiple profile pictures

---

## 🖼️ Image Uploads

### General Image Upload

**Endpoint:** POST `/admin/upload-image`

- Accepts: PNG, JPG, JPEG, GIF, WEBP
- Maximum size: 16MB
- Returns: Image URL for use in projects/content

### Profile Image Upload

**Endpoint:** POST `/admin/update-profile-image`

- Upload up to 4 profile images
- Specify slot (1-4)
- Automatically updates site settings

**Upload Directory:** `backend/app/static/uploads`
**Access URL:** `/admin/uploads/<filename>`

---

## 📝 API Summary

### Public APIs (No Login Required)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/projects` | GET | List all active projects |
| `/api/projects/<id>` | GET | Get single project |
| `/api/resume` | GET | Get resume information |
| `/api/links` | GET | Get all active links |
| `/api/site-settings` | GET | Get site settings |
| `/api/folders` | GET | Get all folders |
| `/api/folders/<id>` | GET | Get folder details |
| `/api/folders/<id>/work` | GET | Get design work in folder |

### Admin APIs (Login Required)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/admin/login` | POST | Admin login |
| `/admin/logout` | POST | Admin logout |
| `/admin/projects` | POST | Create project |
| `/admin/projects/<id>` | PUT | Update project |
| `/admin/projects/<id>` | DELETE | Delete project |
| `/admin/resume` | PUT | Update resume |
| `/admin/links` | POST | Create link |
| `/admin/links/<id>` | PUT | Update link |
| `/admin/links/<id>` | DELETE | Delete link |
| `/admin/settings` | GET | Get settings |
| `/admin/settings` | PUT | Update settings |
| `/admin/upload-image` | POST | Upload image |
| `/admin/update-profile-image` | POST | Upload profile image |
| `/admin/folders` | GET, POST | Manage folders |
| `/admin/folders/<id>` | PUT, DELETE | Update/delete folder |
| `/admin/design-work` | GET, POST | Manage design work |
| `/admin/design-work/<id>` | PUT, DELETE | Update/delete design work |

---

## 🔒 Security Notes

1. **Authentication:** All admin endpoints require login
2. **File Upload:** Only image files allowed (PNG, JPG, GIF, WEBP)
3. **File Size:** Maximum 16MB per upload
4. **CORS:** Enabled only for `/api/*` endpoints
5. **CSRF Protection:** Enabled for all admin forms

---

## 💡 Quick Tips

1. **Change Admin Password:**
   - Login to admin panel
   - Navigate to user settings
   - Update password immediately

2. **Bulk Updates:**
   - Use display_order to control item ordering
   - Use is_active to hide items without deleting

3. **Image Management:**
   - Upload images via admin panel
   - Copy the returned URL
   - Use URL in project/content fields

4. **Database Backup:**
   - Regularly backup your PostgreSQL database
   - See DOCKER.md for backup instructions

---

## 📚 Related Documentation

- [DOCKER.md](DOCKER.md) - Docker deployment guide
- [replit.md](replit.md) - Main project documentation
- [FLASK_MIGRATION.md](FLASK_MIGRATION.md) - Flask migration details

---

**Last Updated:** November 2025
