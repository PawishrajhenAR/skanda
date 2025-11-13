# Vercel Deployment Guide for Skanda Credit Management System

## Overview
This application has been configured for deployment on Vercel's serverless platform. This guide covers the setup and important considerations.

## Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **GitHub Repository**: Your code should be in a GitHub repository
3. **Database**: For production, use **Vercel Postgres** (recommended) or another managed database service

## Important Considerations

### ⚠️ Database Limitations

**SQLite on Vercel:**
- SQLite databases are stored in `/tmp` which is **ephemeral**
- Data will be **lost** between deployments and function invocations
- **NOT suitable for production use**

**Recommended: Use Vercel Postgres**
- Persistent, reliable database
- Free tier available
- Automatically configured with `DATABASE_URL` environment variable

### ⚠️ File Upload Limitations

- Uploaded files are stored in `/tmp/uploads` on Vercel
- Files are **ephemeral** and will be lost between deployments
- For production, consider:
  - AWS S3
  - Cloudinary
  - Vercel Blob Storage
  - Other cloud storage solutions

### ⚠️ EasyOCR Considerations

- **EasyOCR is NOT included in Vercel builds** to prevent Out of Memory (OOM) errors
- EasyOCR requires downloading large models (~500MB+) which causes build failures
- The application works **perfectly without EasyOCR** - OCR features are gracefully disabled
- OCR functionality will show a message that EasyOCR is not available
- For production OCR, consider using:
  - External OCR API services (Google Vision API, AWS Textract, etc.)
  - Separate microservice for OCR processing
  - Client-side OCR libraries

## Deployment Steps

### 1. Connect Repository to Vercel

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click "Add New Project"
3. Import your GitHub repository
4. Select the repository: `PawishrajhenAR/skanda`

### 2. Configure Environment Variables

In Vercel Dashboard → Project Settings → Environment Variables, add:

**Required:**
- `SECRET_KEY`: A secure random string for Flask sessions (generate with: `python -c "import secrets; print(secrets.token_hex(32))"`)

**For Database (if using Vercel Postgres):**
- `DATABASE_URL`: Automatically provided by Vercel Postgres (format: `postgres://...`)

**Optional:**
- `UPLOAD_FOLDER`: Custom upload folder path (default: `/tmp/uploads` on Vercel)

### 3. Set Up Vercel Postgres (Recommended)

1. In Vercel Dashboard → Storage → Create Database
2. Select "Postgres"
3. Choose a plan (Hobby plan is free)
4. The `DATABASE_URL` will be automatically set as an environment variable

### 4. Deploy

1. Vercel will automatically deploy on every push to your main branch
2. Or manually trigger deployment from the dashboard
3. Monitor deployment logs for any issues

## Configuration Files

### vercel.json
- Configured for Python Flask application
- Routes all requests to `wsgi.py`
- Sets `VERCEL=1` environment variable
- Function timeout: 60 seconds
- Memory: 3008 MB (for OCR operations)

### wsgi.py
- Entry point for Vercel
- Exports Flask app as `application`

## Post-Deployment Checklist

- [ ] Verify database connection works
- [ ] Test user login (default: admin/admin123)
- [ ] Test file upload functionality
- [ ] Test OCR functionality (if using)
- [ ] Verify static files are served correctly
- [ ] Check environment variables are set
- [ ] Monitor function logs for errors

## Troubleshooting

### Database Connection Issues
- Verify `DATABASE_URL` is set correctly
- For Vercel Postgres, ensure database is created and linked
- Check connection string format (should start with `postgresql://`)

### File Upload Issues
- Files in `/tmp` are ephemeral - this is expected behavior
- Consider implementing cloud storage for production

### OCR Not Working
- EasyOCR may be too large for Vercel's limits
- Check function logs for initialization errors
- Consider using an external OCR API service

### Function Timeout
- OCR operations can take time
- Current timeout is set to 60 seconds
- For longer operations, consider background jobs or external services

## Production Recommendations

1. **Use Vercel Postgres** instead of SQLite
2. **Implement cloud storage** for file uploads (S3, Cloudinary, etc.)
3. **Use external OCR service** instead of EasyOCR (e.g., Google Vision API, AWS Textract)
4. **Set up monitoring** and error tracking (Sentry, etc.)
5. **Enable HTTPS** (automatic on Vercel)
6. **Set up CI/CD** for automated deployments
7. **Configure backups** for your database

## Support

For issues or questions:
- Check Vercel deployment logs
- Review application logs in Vercel dashboard
- Consult Vercel documentation: https://vercel.com/docs

---

**Last Updated**: December 2024
**Version**: 1.0.0

