# 🚀 DEPLOYMENT GUIDE - AVICENNA HEALTH

**Quick Deploy**: Firebase Hosting in 5 minutes

---

## ⚡ FASTEST OPTION: Firebase Hosting

### Step 1: Install Firebase CLI
```bash
npm install -g firebase-tools
```

### Step 2: Login to Firebase
```bash
firebase login
```

### Step 3: Initialize Firebase Project
```bash
cd c:\Project\AvicennaAI\mobile
firebase init hosting

# Select:
# - Use existing project? → YES (or create new)
# - Public directory? → "build/web"
# - Configure single-page app rewriting? → YES
```

### Step 4: Build Web Version
```bash
flutter build web --release
```

### Step 5: Deploy!
```bash
firebase deploy
```

**Done!** 🎉 Your app is live at: `https://your-project-id.firebaseapp.com`

---

## 🌐 Alternative: Netlify (Easier UI)

### Step 1: Install Netlify CLI
```bash
npm install -g netlify-cli
```

### Step 2: Build Web Version
```bash
cd c:\Project\AvicennaAI\mobile
flutter build web --release
```

### Step 3: Deploy
```bash
netlify deploy --prod --dir=build/web
```

**Done!** 🎉 Your app is live at: `https://your-app.netlify.app`

---

## 📚 GitHub Pages (Free & Simple)

### Step 1: Create GitHub Repository
```bash
git init
git remote add origin https://github.com/username/avicenna-health.git
```

### Step 2: Build with base URL
```bash
cd c:\Project\AvicennaAI\mobile
flutter build web --release --base-href=/avicenna-health/
```

### Step 3: Deploy to gh-pages
```bash
cd build/web
git add .
git commit -m "Deploy web build"
git push -u origin gh-pages
```

**Done!** 🎉 Your app is live at: `https://username.github.io/avicenna-health/`

---

## 🐳 Docker Deployment (Professional)

### Step 1: Create Dockerfile
```dockerfile
FROM nginx:alpine

# Copy web build
COPY build/web /usr/share/nginx/html

# Copy nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
```

### Step 2: Create nginx.conf
```nginx
server {
    listen 80;
    root /usr/share/nginx/html;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

### Step 3: Build Docker Image
```bash
docker build -t avicenna-health:latest .
```

### Step 4: Run Container
```bash
docker run -p 80:80 avicenna-health:latest
```

**Access**: http://localhost

---

## 🏢 Traditional Server (Apache/Nginx)

### Step 1: Build Web Version
```bash
cd c:\Project\AvicennaAI\mobile
flutter build web --release
```

### Step 2: Copy to Server
```bash
# Using SCP
scp -r build/web/* user@your-server:/var/www/avicenna-health/

# Or using SFTP
sftp://user@your-server/var/www/avicenna-health/
```

### Step 3: Configure Server

#### For Nginx
```nginx
server {
    listen 80;
    server_name avicenna-health.com;
    
    root /var/www/avicenna-health;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

#### For Apache
```apache
<Directory /var/www/avicenna-health>
    RewriteEngine On
    RewriteBase /
    RewriteRule ^index\.html$ - [L]
    RewriteCond %{REQUEST_FILENAME} !-f
    RewriteCond %{REQUEST_FILENAME} !-d
    RewriteRule . /index.html [L]
</Directory>
```

### Step 4: Restart Web Server
```bash
# Nginx
sudo systemctl restart nginx

# Apache
sudo systemctl restart apache2
```

---

## 📱 Android Play Store (APK/AAB)

### Step 1: Setup Android SDK
```bash
# Download Android SDK
# Set ANDROID_HOME environment variable
export ANDROID_HOME=/path/to/android/sdk
```

### Step 2: Create App Signing Key
```bash
keytool -genkey -v -keystore ~/app-key.jks \
  -keyalg RSA -keysize 2048 -validity 10000 \
  -alias upload-key
```

### Step 3: Create key.properties
Edit `android/key.properties`:
```properties
storePassword=your_password
keyPassword=your_key_password
keyAlias=upload-key
storeFile=/path/to/app-key.jks
```

### Step 4: Build AAB Bundle
```bash
cd c:\Project\AvicennaAI\mobile
flutter build appbundle --release
```

### Step 5: Upload to Google Play
1. Go to https://play.google.com/console
2. Create new app
3. Upload `build/app/outputs/bundle/release/app-release.aab`
4. Fill app details
5. Submit for review

---

## 🍎 iOS App Store

### Requirements
- Mac with Xcode
- Apple Developer Account ($99/year)
- iOS 11.0+

### Step 1: Configure App
```bash
cd c:\Project\AvicennaAI\mobile
# (Must be on Mac)
flutter build ios --release
```

### Step 2: Sign App
- Open Xcode
- Select Team
- Configure signing

### Step 3: Create IPA
```bash
flutter build ipa --release
```

### Step 4: Upload to App Store
- Use Apple Transporter
- Or TestFlight for beta testing

---

## 🔐 HTTPS/SSL Setup

### Free SSL with Let's Encrypt (Recommended)
```bash
# Using Certbot for Nginx/Apache
sudo apt-get install certbot

# For Nginx
sudo certbot certonly --nginx -d avicenna-health.com

# For Apache
sudo certbot certonly --apache -d avicenna-health.com
```

### Firebase/Netlify
✅ Automatic SSL - No setup needed!

---

## 🔄 Backend API Configuration

### Environment Configuration
Create `.env` file:
```
API_BASE_URL=https://api.avicenna-health.com
API_VERSION=v1
AUTH_TOKEN_KEY=avicenna_token
```

### Update API Service
Edit `lib/services/api_service.dart`:
```dart
static const String baseUrl = 'https://api.avicenna-health.com/api';
```

---

## 📊 Monitoring & Analytics

### Google Analytics
```bash
# Add analytics package
flutter pub add firebase_analytics

# Initialize in main.dart
FirebaseAnalytics.instance.logAppOpen();
```

### Crash Reporting
```bash
# Add Crashlytics
flutter pub add firebase_crashlytics

# Initialize in main.dart
FirebaseCrashlytics.instance.recordFlutterError(details);
```

### Custom Logging
```bash
# Already configured in services
print('📊 Event logged');
```

---

## 🧪 Testing After Deployment

### Functional Testing
```bash
# Test all screens
# Verify API calls work
# Check database operations
# Test permissions
# Verify offline mode
```

### Performance Testing
```bash
# Check load time (should be <3 seconds)
# Monitor memory usage
# Test on slow connections (3G)
# Verify image compression
```

### Security Testing
```bash
# Test permission boundaries
# Verify data encryption
# Check API token handling
# Test error messages (no sensitive data)
```

---

## 🚨 Troubleshooting

### Build Fails
```bash
flutter clean
flutter pub get
flutter build web --release -v
```

### Deploy Fails
```bash
# Check file permissions
chmod -R 755 build/web/

# Verify all files copied
ls -la build/web/
```

### App Won't Load
```bash
# Check browser console (F12)
# Check server logs
# Verify CORS settings
# Check API endpoint configuration
```

### Slow Performance
```bash
# Enable compression
# Optimize images
# Check network tab (F12)
# Profile with DevTools
```

---

## 📈 Performance Optimization

### Web Build Size
```bash
# Analyze size
flutter build web --release --analyze-size

# Typical: 50-100 MB
# With compression: 15-30 MB
```

### Gzip Compression
```nginx
# Add to nginx.conf
gzip on;
gzip_types text/plain application/json application/javascript text/css;
gzip_min_length 1000;
```

### Caching Strategy
```nginx
# Static files
location /assets/ {
    expires 365d;
}

# HTML (always fresh)
location ~* ^(?!.*?\.(?:css|js|jpg|jpeg|png|gif|webp)).*?$ {
    expires -1;
}
```

---

## ✅ DEPLOYMENT CHECKLIST

- [ ] Web build successful
- [ ] All assets included
- [ ] API endpoints updated
- [ ] Environment variables set
- [ ] SSL certificate configured
- [ ] Database migrations run
- [ ] Monitoring setup
- [ ] Backup created
- [ ] Deployment tested
- [ ] Go-live approved

---

## 📱 QUICK DECISION MATRIX

| Platform | Setup Time | Cost | Recommendation |
|----------|-----------|------|---|
| **Firebase** | 5 min | Free | ⭐⭐⭐⭐⭐ Best |
| **Netlify** | 5 min | Free | ⭐⭐⭐⭐ Easy |
| **GitHub Pages** | 10 min | Free | ⭐⭐⭐⭐ Good |
| **Docker** | 20 min | Varies | ⭐⭐⭐ Professional |
| **Traditional Server** | 30 min | Varies | ⭐⭐⭐ Control |

---

## 🎯 RECOMMENDED PATH

```
1. Firebase Hosting (Immediate)
   ↓
2. API Backend Setup (1 week)
   ↓
3. Google Play Store (2 weeks)
   ↓
4. Apple App Store (3 weeks)
   ↓
5. Advanced Monitoring (1 month)
```

---

**Last Updated**: December 16, 2025
**Ready to Deploy?** Start with Firebase! 🚀
