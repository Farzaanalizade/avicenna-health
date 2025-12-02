# GitHub Actions APK Build - Step by Step

## English Version

### Prerequisites
- GitHub account (free: https://github.com/signup)
- Git installed on your machine
- Your project code ready

### Step 1: Create GitHub Account & Repository

1. Go to https://github.com/signup
2. Fill in username, email, password
3. Click "Create account"
4. Create new repository:
   - Name: `avicenna-health`
   - Description: "Avicenna Health - Mobile App"
   - Visibility: Public (for free Actions)
   - Initialize: Empty repository

### Step 2: Push Your Code to GitHub

Open PowerShell in `d:\AvicennaAI`:

```powershell
cd d:\AvicennaAI

# Configure Git (one time)
git config --global user.name "Your Name"
git config --global user.email "your.email@gmail.com"

# Initialize repository
git init
git add .
git commit -m "Initial commit - Avicenna Health App"
git branch -M main

# Add GitHub remote
git remote add origin https://github.com/YOUR_USERNAME/avicenna-health.git

# Push to GitHub
git push -u origin main

# When prompted for password:
# - Use Personal Access Token instead of password
# - Go to: https://github.com/settings/tokens/new
# - Click "Generate new token"
# - Check: "repo" scope
# - Copy token and paste as password
```

### Step 3: Verify Files on GitHub

1. Go to https://github.com/YOUR_USERNAME/avicenna-health
2. Check if `.github/workflows/build-apk.yml` exists
3. If not, create it:
   - Click "Add file" → "Create new file"
   - Name: `.github/workflows/build-apk.yml`
   - Copy content from: `d:\AvicennaAI\.github\workflows\build-apk.yml`
   - Click "Commit new file"

### Step 4: Run the Build

1. Go to: https://github.com/YOUR_USERNAME/avicenna-health/actions
2. Left sidebar → Click "Build APK"
3. Top right → Click "Run workflow"
4. Select branch: `main`
5. Click green "Run workflow" button

### Step 5: Wait & Download

1. Watch the build progress (should take 15-20 minutes)
2. When complete, click the workflow run
3. Scroll down to "Artifacts" section
4. Download:
   - `avicenna-health-release.apk` (for production)
   - `avicenna-health-debug.apk` (for testing)

### Step 6: Install on Android Phone

```powershell
# Connect phone via USB cable
# Enable USB Debugging:
#   Settings → About Phone → Tap "Build Number" 7 times
#   Back → Developer options → Enable "USB Debugging"

adb devices  # Should show your device

# Install APK
adb install -r avicenna-health-release.apk

# Or via file explorer - copy APK to phone and tap to install
```

### Step 7: Test the App

1. Tap app icon on home screen
2. See splash screen
3. Login/Register
4. Test health analysis features

---

## Farsi Version (فارسی)

### پیش‌نیازها
- حساب GitHub (رایگان: https://github.com/signup)
- Git نصب شده
- کدهای پروژه آماده

### مرحله 1: ایجاد حساب و مخزن GitHub

1. به https://github.com/signup بروید
2. نام کاربری، ایمیل، رمز را پر کنید
3. روی "Create account" کلیک کنید
4. مخزن جدید بسازید:
   - نام: `avicenna-health`
   - توضیح: "Avicenna Health - Mobile App"
   - عمومی: بله (برای استفاده رایگان)
   - خالی بسازید

### مرحله 2: فرستادن کدها به GitHub

PowerShell را در `d:\AvicennaAI` باز کنید:

```powershell
cd d:\AvicennaAI

# تنظیم Git (یک بار)
git config --global user.name "نام شما"
git config --global user.email "ایمیل@gmail.com"

# شروع مخزن
git init
git add .
git commit -m "Initial commit - Avicenna Health App"
git branch -M main

# اضافه کردن آدرس GitHub
git remote add origin https://github.com/نام_کاربری_شما/avicenna-health.git

# فرستادن به GitHub
git push -u origin main

# وقتی برای رمز بپرسد:
# - توکن شخصی استفاده کنید نه رمز
# - به: https://github.com/settings/tokens/new بروید
# - "Generate new token" را کلیک کنید
# - "repo" را انتخاب کنید
# - توکن را کپی و به‌عنوان رمز بچسبانید
```

### مرحله 3: بررسی در GitHub

1. به https://github.com/نام_کاربری/avicenna-health بروید
2. چک کنید `.github/workflows/build-apk.yml` موجود است
3. اگر نه، بسازید:
   - "Add file" → "Create new file"
   - نام: `.github/workflows/build-apk.yml`
   - محتوا: کپی از `d:\AvicennaAI\.github\workflows\build-apk.yml`
   - "Commit new file" کلیک کنید

### مرحله 4: شروع Build

1. به https://github.com/نام_کاربری/avicenna-health/actions بروید
2. سمت چپ → "Build APK" کلیک کنید
3. بالا سمت راست → "Run workflow"
4. شاخه: `main`
5. دکمه سبز "Run workflow"

### مرحله 5: انتظار و دانلود

1. پیشرفت را نگاه کنید (15-20 دقیقه)
2. وقتی تمام شد، workflow را کلیک کنید
3. پایین → بخش "Artifacts"
4. دانلود کنید:
   - `avicenna-health-release.apk` (برای استفاده)
   - `avicenna-health-debug.apk` (برای تست)

### مرحله 6: نصب روی گوشی Android

```powershell
# گوشی را به کابل USB وصل کنید
# USB Debugging را فعال کنید:
#   تنظیمات → درباره گوشی → 7 بار روی Build Number ضربه بزنید
#   برگردید → Developer options → USB Debugging را روشن کنید

adb devices  # باید گوشی را نشان دهد

# نصب APK
adb install -r avicenna-health-release.apk

# یا از طریق فایل‌منجر - APK را به گوشی کپی و ضربه بزنید
```

### مرحله 7: تست اپلیکیشن

1. روی نماد اپ ضربه بزنید
2. صفحه شروع را ببینید
3. وارد یا ثبت‌نام کنید
4. ویژگی‌های تحلیل سلامتی را تست کنید

---

## Troubleshooting

### GitHub push fails with "authentication failed"

```powershell
# Generate Personal Access Token:
# 1. Go to: https://github.com/settings/tokens
# 2. Click "Generate new token"
# 3. Name: "git-push"
# 4. Scope: Check "repo"
# 5. Copy token
# 6. Re-run git push, use token as password
```

### Build fails in GitHub Actions

Common fixes:
1. Check `.github/workflows/build-apk.yml` syntax
2. Ensure `pubspec.yaml` exists in root
3. Check `android/app/build.gradle` exists
4. View logs: Click workflow run → Click "build" step

### APK installation fails on phone

```bash
# Clear previous installation
adb uninstall com.example.avicenna_health

# Reinstall
adb install -r avicenna-health-release.apk
```

---

## Files & References

| File | Purpose |
|------|---------|
| `.github/workflows/build-apk.yml` | Workflow configuration |
| `pubspec.yaml` | Flutter dependencies |
| `android/app/build.gradle` | Android build config |
| `lib/main.dart` | App entry point |

---

## Time Estimates

| Task | Duration |
|------|----------|
| Create GitHub account | 5 min |
| Push code | 5-10 min |
| Run build | 15-20 min |
| Download APK | 1 min |
| Install on phone | 2-3 min |
| **Total** | **30-40 min** |

---

## Success Indicators

✅ GitHub account created
✅ Code pushed to GitHub
✅ `.github/workflows/build-apk.yml` exists in repo
✅ Build workflow shows "completed" (green checkmark)
✅ APK downloaded from artifacts
✅ APK installed on Android phone
✅ App launches and shows splash screen

---

**Questions?** Check:
- GitHub Actions docs: https://docs.github.com/en/actions
- Flutter Android docs: https://flutter.dev/docs/deployment/android
- ADB commands: https://developer.android.com/studio/command-line/adb

