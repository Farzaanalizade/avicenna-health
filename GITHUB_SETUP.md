# 🚀 GITHUB SETUP - برای Codemagic

## ✅ مراحل نهایی برای GitHub Upload

---

## **Step 1: GitHub Account**

اگر ندارید:
```
https://github.com/signup
```https://codemagic.io
1. Sign in (GitHub سے)
2. Select: avicenna-health
3. Set up build (Android)
4. Build شروع کرو
5. APK download (5-10 min)
6. گوشی میں install

---

## **Step 2: Create New Repository**

```
https://github.com/new
```

**یا اینجا:**
1. GitHub.com میں login کن
2. "+" آئیکن (Top right)
3. "New repository"

**Settings:**
```
Repository name: avicenna-health

Description: Avicenna Health - Traditional Persian Medicine Diagnostic App

Visibility: Public (برای Codemagic)

.gitignore: Dart

License: MIT (یا درخواستی)
```

**Create Repository کلیک کن ✓**

---

## **Step 3: GitHub میں Repository اضافہ**

### (Already Done Locally - Just Push Now)

```bash
cd c:\Project\AvicennaAI

# Remote add (تبدیل کن USERNAME و REPO_NAME)
git remote add origin https://github.com/USERNAME/avicenna-health.git

# Branch rename (اختیاری)
git branch -M main

# Push to GitHub
https://codemagic.io
1. Sign in (GitHub سے)
2. Select: avicenna-health
3. Set up build (Android)
4. Build شروع کرو
5. APK download (5-10 min)
6. گوشی میں install
```

---

## **Step 4: Generate GitHub Token (For Codemagic)**

```
https://github.com/settings/tokens
```

**یا:**
1. GitHub → Settings (Top right)
2. Developer settings (Left sidebar)
3. Personal access tokens → Tokens (classic)
4. "Generate new token (classic)"

**Scopes Select:**
```
✓ repo (Full control of private repositories)
✓ admin:repo_hook (Write access to hooks)
✓ user:email (Access email addresses)
```

**Generate Token**
- Token copy کن (صرف ایک بار دیکھ سکتے ہو!)
- کسی safe جگہ محفوظ کن

---

## **Step 5: Verify on GitHub**

```
https://github.com/USERNAME/avicenna-health
```

**چیک کن:**
- [ ] Repository دیکھ رہے ہیں
- [ ] تمام فایل‌ها موجود ہیں
- [ ] mobile/ folder دیکھ رہے ہیں
- [ ] pubspec.yaml موجود ہے
- [ ] lib/ folder موجود ہے

---

## **Step 6: Codemagic Connect**

### https://codemagic.io

```
1. Sign up / Login (GitHub سے)
2. "Connect repository"
3. Select: avicenna-health
4. "Set up build"
5. Platform: Android
6. "Save"
7. "Build"
```

**Wait 5-10 minutes**

---

## **نتیجه:**

✅ GitHub میں repo
✅ تمام files uploaded
✅ Ready برای Codemagic
✅ Automatic builds

---

## 🎯 Quick Commands

```bash
# Already done locally - Just push:

cd c:\Project\AvicennaAI

# Set remote
git remote add origin https://github.com/YOUR_USERNAME/avicenna-health.git

# Push to GitHub
git push -u origin main

# Verify
git remote -v
```

---

## 📝 NEXT STEPS

```
1. ✅ Create GitHub repo
2. ✅ Push local code
3. ✅ Generate token
4. 👉 Go to Codemagic
5. 👉 Connect GitHub
6. 👉 Build APK
7. 👉 Download & Install
```

---

## 🆘 Issues?

### "Remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/avicenna-health.git
```

### "Authentication failed"
```bash
# Use token instead of password:
# URL: https://your_token@github.com/YOUR_USERNAME/avicenna-health.git
```

### "Branch main doesn't exist"
```bash
git branch -M main
git push -u origin main
```

---

**Ready? Start: https://github.com/new 🚀**

**Then: https://codemagic.io 🎉**

---
