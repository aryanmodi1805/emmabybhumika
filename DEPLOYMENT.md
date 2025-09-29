# Railway Deployment Guide

This guide will help you deploy your Django backend to Railway.com.

## Prerequisites

1. A Railway account (sign up at https://railway.app)
2. Git repository (GitHub, GitLab, or Bitbucket)
3. Your backend code pushed to the repository

## Deployment Steps

### 1. Push Your Code to Git Repository

Make sure your backend code is pushed to a Git repository (GitHub, GitLab, or Bitbucket).

### 2. Connect Railway to Your Repository

1. Go to https://railway.app and sign in
2. Click "New Project"
3. Select "Deploy from GitHub repo" (or your preferred Git provider)
4. Choose your repository
5. Railway will automatically detect it's a Python/Django project

### 3. Add PostgreSQL Database

1. In your Railway project dashboard, click "New"
2. Select "Database" → "PostgreSQL"
3. Railway will automatically create a PostgreSQL database
4. Note down the connection details (they'll be available as environment variables)

### 4. Configure Environment Variables

In your Railway project settings, add these environment variables:

#### Required Environment Variables:
- `SECRET_KEY`: Generate a new secret key for production
- `DJANGO_SETTINGS_MODULE`: Set to `fashion_backend.production`

#### Database Variables (automatically provided by Railway PostgreSQL):
- `DATABASE_URL`: Automatically set by Railway
- `DATABASE_NAME`: Automatically set by Railway
- `DATABASE_USER`: Automatically set by Railway
- `DATABASE_PASSWORD`: Automatically set by Railway
- `DATABASE_HOST`: Automatically set by Railway
- `DATABASE_PORT`: Automatically set by Railway

#### Optional Environment Variables:
- `PORT`: Railway will set this automatically
- `RAILWAY_STATIC_URL`: For static files (if needed)

### 5. Generate a New Secret Key

Run this command to generate a new secret key:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Add this as the `SECRET_KEY` environment variable in Railway.

### 6. Deploy

1. Railway will automatically deploy when you push changes to your repository
2. You can also trigger a manual deployment from the Railway dashboard
3. Check the deployment logs for any issues

### 7. Configure Custom Domain (Optional)

1. In Railway dashboard, go to your service
2. Click on "Settings" → "Domains"
3. Add your custom domain
4. Update DNS records as instructed

## File Structure for Railway

Your backend should have this structure:
```
backend/
├── manage.py
├── requirements.txt
├── Procfile
├── runtime.txt
├── railway.toml
├── fashion_backend/
│   ├── __init__.py
│   ├── settings.py
│   ├── production.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── fashion_images/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── ...
└── media/
    └── ...
```

## Troubleshooting

### Common Issues:

1. **Build Failures**: Check that all dependencies are in `requirements.txt`
2. **Database Connection**: Ensure PostgreSQL is added as a service
3. **Static Files**: Make sure `whitenoise` is in requirements and middleware is configured
4. **CORS Issues**: Update `CORS_ALLOWED_ORIGINS` in production settings

### Useful Commands:

```bash
# Check deployment logs
railway logs

# Connect to Railway CLI (if installed)
railway login
railway link
```

## Environment Variables Reference

| Variable | Description | Required | Auto-set by Railway |
|----------|-------------|----------|-------------------|
| `SECRET_KEY` | Django secret key | Yes | No |
| `DJANGO_SETTINGS_MODULE` | Django settings module | Yes | No |
| `DATABASE_URL` | Database connection URL | Yes | Yes |
| `DATABASE_NAME` | Database name | Yes | Yes |
| `DATABASE_USER` | Database user | Yes | Yes |
| `DATABASE_PASSWORD` | Database password | Yes | Yes |
| `DATABASE_HOST` | Database host | Yes | Yes |
| `DATABASE_PORT` | Database port | Yes | Yes |
| `PORT` | Application port | Yes | Yes |

## Next Steps

After successful deployment:
1. Test your API endpoints
2. Update your frontend to use the new Railway URL
3. Set up monitoring and logging
4. Configure backups for your database
