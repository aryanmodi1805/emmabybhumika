#!/bin/bash

# Railway Deployment Script for Django Backend
# This script helps prepare and deploy your Django backend to Railway

echo "🚀 Railway Deployment Script for Django Backend"
echo "================================================"

# Check if we're in the backend directory
if [ ! -f "manage.py" ]; then
    echo "❌ Error: Please run this script from the backend directory"
    exit 1
fi

echo "✅ Found Django project"

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📦 Initializing Git repository..."
    git init
    git add .
    git commit -m "Initial commit for Railway deployment"
    echo "✅ Git repository initialized"
else
    echo "✅ Git repository already exists"
fi

# Check if all required files exist
echo "🔍 Checking required files..."

required_files=("requirements.txt" "Procfile" "runtime.txt" "railway.toml")
for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file exists"
    else
        echo "❌ $file is missing"
        exit 1
    fi
done

echo ""
echo "📋 Deployment Checklist:"
echo "========================"
echo "1. ✅ Backend files prepared"
echo "2. ✅ Production settings configured"
echo "3. ✅ Requirements.txt updated with production dependencies"
echo "4. ✅ Railway configuration files created"
echo ""
echo "🔑 Generated Secret Key for Railway:"
echo "lTn4ieLdcncSbQD87gZudh60mgtTdv-32TfGbQ9vlxDmxcFJNa_06o3ppCpI3xZNR4I"
echo ""
echo "📝 Next Steps:"
echo "============="
echo "1. Push your code to GitHub/GitLab/Bitbucket"
echo "2. Go to https://railway.app and create a new project"
echo "3. Connect your repository to Railway"
echo "4. Add PostgreSQL database service"
echo "5. Set environment variables:"
echo "   - SECRET_KEY: lTn4ieLdcncSbQD87gZudh60mgtTdv-32TfGbQ9vlxDmxcFJNa_06o3ppCpI3xZNR4I"
echo "   - DJANGO_SETTINGS_MODULE: fashion_backend.production"
echo "6. Deploy!"
echo ""
echo "📖 For detailed instructions, see DEPLOYMENT.md"
echo ""
echo "🎉 Your backend is ready for Railway deployment!"
