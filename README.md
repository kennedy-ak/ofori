# Ofori Blog

A complete Django-based blog platform with user management, rich text editing, newsletter system, and more.

## Features

### User Management
- User registration with automatic profile creation
- Login/logout functionality
- User approval workflow (admin approval required before posting)
- User profiles with bio, profile image, and approval status

### Blog System
- Create, edit, and delete blog posts
- Rich text editor (Summernote WYSIWYG)
- Categories: Technology, Politics, Life, Advice, Others
- Featured image upload
- Draft and Published status
- Automatic slug generation
- Reading time calculation
- Excerpt generation

### Interaction Features
- Like/unlike posts
- Like count display
- Search functionality (title and content)

### Newsletter System
- Email subscription with unique constraint
- Automated welcome emails
- Automated notifications when new posts are published
- Resubscribe with welcome back email
- Unsubscribe functionality
- Unsubscribe link in all emails

### Dashboards
- User Dashboard: View all posts, statistics, quick actions
- Admin Dashboard: Manage user approvals

## Technology Stack

- Django 5.2.6
- SQLite database
- django-summernote (rich text editor)
- django-cors-headers
- Pillow (image handling)
- python-decouple (environment variables)
- Bootstrap 5 (frontend)

## Installation

### Prerequisites
- Python 3.8 or higher
- pip

### Setup Instructions

1. **Clone or download the project**
   ```bash
   cd ofori
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Mac/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```

   Edit `.env` file and add your configuration:
   - SECRET_KEY: Django secret key
   - EMAIL_HOST_USER: Your Gmail address
   - EMAIL_HOST_PASSWORD: Gmail app password (not your regular password)
   - DEFAULT_FROM_EMAIL: Email address to send from

   **Note**: For Gmail, you need to create an App Password:
   1. Go to Google Account settings
   2. Security → 2-Step Verification
   3. App passwords → Generate new app password
   4. Use this password in EMAIL_HOST_PASSWORD

6. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

7. **Create a superuser (admin)**
   ```bash
   python manage.py createsuperuser
   ```

8. **Run the development server**
   ```bash
   python manage.py runserver
   ```

9. **Access the application**
   - Website: http://127.0.0.1:8000/
   - Admin: http://127.0.0.1:8000/admin/

## Usage

### For Regular Users

1. **Register** an account at `/register/`
2. **Wait for admin approval** (check with admin)
3. **Create posts** once approved
4. **Like posts** from other users
5. **Search** for posts using the search bar

### For Admins

1. **Login** to the Django admin at `/admin/`
2. **Approve users** from the Admin Dashboard at `/admin-dashboard/`
3. **Manage content** through the Django admin interface
4. **View pending approvals** in the Admin Dashboard

### Newsletter

- Subscribe using the form in the footer
- Receive welcome email upon subscription
- Get notifications when new posts are published
- Unsubscribe using the link in any email

## URL Structure

- `/` - Home page (all published posts)
- `/register/` - User registration
- `/login/` - Login
- `/logout/` - Logout
- `/post/create/` - Create new post (approved users only)
- `/post/<slug>/` - View post
- `/post/<slug>/edit/` - Edit post
- `/post/<slug>/delete/` - Delete post
- `/post/<slug>/like/` - Like/unlike post
- `/search/` - Search posts
- `/user/<username>/` - User profile
- `/dashboard/` - User dashboard
- `/admin-dashboard/` - Admin dashboard
- `/newsletter/subscribe/` - Subscribe to newsletter
- `/newsletter/unsubscribe/<email>/` - Unsubscribe
- `/admin/` - Django admin

## Models

### UserProfile
- Extends Django User model
- Fields: is_approved, bio, profile_image, approved_at, created_at

### Post
- Fields: title, slug, author, content, category, image, status, created_at, updated_at
- Methods: get_reading_time(), get_excerpt(), get_like_count()

### Like
- Fields: post, user, created_at
- Unique constraint on (post, user)

### Newsletter
- Fields: email, is_active, subscribed_at, unsubscribed_at

## Development

### Project Structure
```
ofori/
├── ofori_blog/          # Project settings
├── users/               # User management app
├── blog/                # Blog posts app
├── newsletter/          # Newsletter app
├── templates/           # HTML templates
├── static/              # Static files (CSS, JS)
├── media/               # User uploads
├── requirements.txt     # Dependencies
├── .env.example         # Environment variables template
├── .gitignore          # Git ignore file
└── README.md           # This file
```

### Creating Migrations

After modifying models:
```bash
python manage.py makemigrations
python manage.py migrate
```

### Collecting Static Files (Production)

```bash
python manage.py collectstatic
```

## Deployment

For production deployment:

1. Set `DEBUG=False` in `.env`
2. Set proper `SECRET_KEY` in `.env`
3. Configure email settings in `.env`
4. Set up a proper database (PostgreSQL recommended)
5. Configure web server (nginx/Apache)
6. Set up WSGI server (Gunicorn/uWSGI)
7. Enable HTTPS
8. Run `python manage.py collectstatic`

## Security Notes

- Never commit `.env` file to version control
- Use strong SECRET_KEY in production
- Enable HTTPS in production
- Use app passwords for Gmail (not your main password)
- Keep dependencies updated
- Regular database backups

## Support

For issues or questions, please refer to the Django documentation:
- https://docs.djangoproject.com/

## License

This project is created for educational and portfolio purposes.

## Author

Ofori Blog Platform - 2024
