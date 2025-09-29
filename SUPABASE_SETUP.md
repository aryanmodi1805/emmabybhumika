# Supabase Integration Setup Guide

## 🚀 **Setting Up Supabase for Image Storage**

### **Step 1: Create Supabase Project**
1. Go to [https://supabase.com](https://supabase.com)
2. Sign up/Login with your account
3. Click "New Project"
4. Choose your organization
5. Enter project details:
   - **Name**: `fashion-images-storage`
   - **Database Password**: Generate a strong password
   - **Region**: Choose closest to your users
6. Click "Create new project"

### **Step 2: Create Storage Bucket**
1. In your Supabase dashboard, go to **Storage**
2. Click **"New bucket"**
3. Enter bucket details:
   - **Name**: `fashion-images`
   - **Public**: ✅ Check this (so images can be accessed publicly)
4. Click **"Create bucket"**

### **Step 3: Get API Keys**
1. Go to **Settings** → **API**
2. Copy the following values:
   - **Project URL**: `https://your-project-id.supabase.co`
   - **anon public key**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`

### **Step 4: Configure Railway Environment Variables**
In your Railway project, add these environment variables:

```
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_BUCKET_NAME=fashion-images
```

### **Step 5: Upload Images to Supabase**
You can upload images in two ways:

#### **Option A: Using Supabase Dashboard**
1. Go to **Storage** → **fashion-images** bucket
2. Click **"Upload file"**
3. Upload your images
4. Copy the public URLs

#### **Option B: Using Django Management Command**
```bash
python manage.py migrate_to_supabase
```

### **Step 6: Update Database Records**
After uploading to Supabase, update your database records with the Supabase URLs:

```python
# Example: Update FashionImage records
from fashion_images.models import FashionImage

# Update each image with its Supabase URL
image = FashionImage.objects.get(id=1)
image.image_url = "https://your-project.supabase.co/storage/v1/object/public/fashion-images/image1.jpg"
image.save()
```

## 🔧 **API Endpoints**

### **Card Data API**
- **URL**: `/api/card-data/`
- **Method**: GET
- **Response**: Returns team members with Supabase image URLs

### **Media Files API**
- **URL**: `/api/media-files/`
- **Method**: GET
- **Response**: Returns all media files with Supabase URLs

### **Media List API**
- **URL**: `/api/media-files/media_list/`
- **Method**: GET
- **Response**: Returns simplified media file list

## 📋 **Benefits of Supabase Storage**

✅ **Scalable**: Handle large files without server storage limits  
✅ **Fast**: Global CDN for fast image delivery  
✅ **Reliable**: 99.9% uptime guarantee  
✅ **Secure**: Built-in access controls  
✅ **Cost-effective**: Pay only for what you use  
✅ **Easy integration**: Simple API for uploads/downloads  

## 🚀 **Deployment Benefits**

- **Smaller deployment size**: No large media files in your codebase
- **Faster deployments**: Railway doesn't need to upload large files
- **Better performance**: Images served from Supabase CDN
- **Scalable storage**: No server storage limitations

## 🔍 **Testing Your Setup**

1. **Check environment variables**:
   ```bash
   python manage.py shell
   >>> from fashion_images.supabase_service import supabase_storage
   >>> print(supabase_storage.client is not None)
   ```

2. **Test image upload**:
   ```bash
   python manage.py migrate_to_supabase --dry-run
   ```

3. **Check API responses**:
   - Visit `/api/card-data/` to see Supabase URLs
   - Visit `/api/media-files/` to see media file URLs

## 🛠️ **Troubleshooting**

### **Common Issues:**

1. **"Supabase client not available"**
   - Check environment variables are set correctly
   - Verify Supabase URL and key are valid

2. **"Failed to upload file"**
   - Check bucket exists and is public
   - Verify file permissions
   - Check file size limits

3. **"File not found"**
   - Verify local file paths are correct
   - Check MEDIA_ROOT setting

### **Debug Commands:**
```bash
# Check Supabase connection
python manage.py shell
>>> from fashion_images.supabase_service import supabase_storage
>>> print(supabase_storage.supabase_url)
>>> print(supabase_storage.bucket_name)

# Test migration
python manage.py migrate_to_supabase --dry-run
```
