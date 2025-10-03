# BlockHire Deployment Guide

## 🚀 Render Deployment Instructions

### Prerequisites
- GitHub repository with BlockHire code
- Render account (free tier available)

### Step 1: Backend Deployment

1. **Create New Web Service on Render**
   - Go to Render Dashboard
   - Click "New +" → "Web Service"
   - Connect your GitHub repository

2. **Backend Configuration**
   - **Name**: `blockhire-backend`
   - **Environment**: `Python 3`
   - **Build Command**: 
     ```bash
     cd backend
     pip install -r requirements.txt
     python manage.py collectstatic --noinput
     python manage.py migrate
     ```
   - **Start Command**: 
     ```bash
     cd backend
     python manage.py runserver 0.0.0.0:$PORT
     ```

3. **Environment Variables**
   ```
   DJANGO_SETTINGS_MODULE=blockhire.settings
   SECRET_KEY=[Generate secure key]
   DEBUG=False
   ALLOWED_HOSTS=blockhire-backend.onrender.com
   DATABASE_URL=[Auto-generated PostgreSQL URL]
   CORS_ALLOWED_ORIGINS=https://blockhire-frontend.onrender.com
   JWT_SECRET_KEY=[Generate secure key]
   ```

### Step 2: Frontend Deployment

1. **Create New Web Service on Render**
   - **Name**: `blockhire-frontend`
   - **Environment**: `Node`
   - **Build Command**: 
     ```bash
     cd frontend
     npm install
     npm run build
     ```
   - **Start Command**: 
     ```bash
     cd frontend
     npm start
     ```

2. **Environment Variables**
   ```
   NEXT_PUBLIC_API_URL=https://blockhire-backend.onrender.com/api
   ```

### Step 3: Database Setup

1. **Create PostgreSQL Database**
   - Go to Render Dashboard
   - Click "New +" → "PostgreSQL"
   - **Name**: `blockhire-db`
   - **Plan**: Free tier

2. **Connect Database to Backend**
   - Use the auto-generated `DATABASE_URL` in backend environment variables

### Step 4: Domain Configuration

1. **Backend URL**: `https://blockhire-backend.onrender.com`
2. **Frontend URL**: `https://blockhire-frontend.onrender.com`

### Step 5: Post-Deployment Setup

1. **Create Superuser**
   ```bash
   # Access backend service shell on Render
   python manage.py createsuperuser
   ```

2. **Verify Deployment**
   - Backend API: `https://blockhire-backend.onrender.com/api/test/`
   - Frontend App: `https://blockhire-frontend.onrender.com`

## 🔧 Production Optimizations

### Backend Optimizations
- ✅ Gunicorn for production WSGI server
- ✅ WhiteNoise for static file serving
- ✅ Security headers configured
- ✅ Database connection pooling
- ✅ Static file compression

### Frontend Optimizations
- ✅ Next.js standalone output
- ✅ Production build optimization
- ✅ Environment variable configuration
- ✅ Static asset optimization

## 📊 Monitoring & Maintenance

### Health Checks
- Backend: `GET /api/test/`
- Frontend: Root URL should load

### Logs
- Access logs through Render Dashboard
- Monitor for errors and performance issues

### Updates
- Push changes to GitHub
- Render will automatically redeploy
- Database migrations run automatically

## 🛡️ Security Considerations

### Production Security
- ✅ HTTPS enforced
- ✅ Security headers configured
- ✅ CORS properly configured
- ✅ JWT tokens with secure keys
- ✅ Database credentials secured

### Environment Variables
- Never commit `.env` files
- Use Render's environment variable system
- Rotate secrets regularly

## 🚨 Troubleshooting

### Common Issues

1. **Build Failures**
   - Check Python/Node versions
   - Verify all dependencies in requirements.txt
   - Check build logs for specific errors

2. **Database Connection Issues**
   - Verify DATABASE_URL is set correctly
   - Check PostgreSQL service is running
   - Run migrations manually if needed

3. **CORS Errors**
   - Verify CORS_ALLOWED_ORIGINS includes frontend URL
   - Check backend CORS configuration

4. **Static Files Not Loading**
   - Verify WhiteNoise configuration
   - Check STATIC_ROOT setting
   - Run collectstatic command

### Support
- Check Render documentation
- Review application logs
- Test locally first before deploying

## 🎉 Success Checklist

- [ ] Backend API responding
- [ ] Frontend loading correctly
- [ ] Database connected
- [ ] User registration working
- [ ] Document upload working
- [ ] Verification system working
- [ ] All environment variables set
- [ ] HTTPS enabled
- [ ] Security headers active

Your BlockHire application is now ready for production! 🚀
