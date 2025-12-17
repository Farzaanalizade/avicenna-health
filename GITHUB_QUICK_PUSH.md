# 📤 PUSH TO GITHUB - فوری راهنما

## ✅ STEPS (3 دقیقه)

---

## **Step 1: Create GitHub Repo**

```
https://github.com/new
```

**Fill:**
```
Name: avicenna-health
Visibility: Public
```

**Create Repository ✓**

---

## **Step 2: Copy Your Username**

Example:
```
https://github.com/YOUR_USERNAME/avicenna-health
```

جایے `YOUR_USERNAME` اپنا username لکھو!

---

## **Step 3: Push Code (Windows PowerShell)**

```powershell
cd c:\Project\AvicennaAI

# 1. Add remote (تبدیل USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/avicenna-health.git

# 2. Rename branch to 'main'
git branch -M main

# 3. Push to GitHub
git push -u origin main
```

**Wait for upload... (1-2 minutes)**

---

## **Step 4: Verify**

```
https://github.com/YOUR_USERNAME/avicenna-health
```

✅ دیکھیں تمام فایل‌ها uploaded ہیں؟

---

## 🎯 Codemagic اب Ready ہے!

```
https://codemagic.io
→ Sign in with GitHub
→ Select: avicenna-health
→ Build!
```

---

**Done! 🎉**

---
