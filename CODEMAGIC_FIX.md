# 🔧 CODEMAGIC FIX - pubspec.yaml نہ ملا

## ⚠️ مسئلہ:
```
Failed to install dependencies for pubspec file
in /Users/builder/clone
```

## ✅ حل:

### Step 1: Codemagic میں جا
```
https://codemagic.io/app/avicenna-health
```

### Step 2: Settings اونجا
```
1. "avicenna-health" app click
2. "Settings" (gear icon)
3. "Build" section
```

### Step 3: Project Root Path set کرو

**Find:**
```
Project root path
```

**Change to:**
```
mobile
```

### Step 4: Save & Rebuild

```
1. "Save" click
2. "Start new build" click
3. Wait 5-10 minutes
```

---

## یا اگر یہ کام نہیں کرے:

### codemagic.yaml بنا

Project root میں بنا: `codemagic.yaml`

```yaml
workflows:
  avicenna-health:
    name: Avicenna Health Build
    environment:
      android_signing:
        - avicenna_health_key
      vars:
        PACKAGE_NAME: "com.avicenna.health"
    triggering:
      events:
        - push
      branch:
        include:
          - main
    scripts:
      - name: Set Java version
        script: |
          jenv versions
          jenv global 11
      
      - name: Get Flutter packages
        script: |
          cd mobile
          flutter pub get
      
      - name: Build APK
        script: |
          cd mobile
          flutter build apk --debug
    
    artifacts:
      - mobile/build/app/outputs/flutter-apk/app-debug.apk
    
    publishing:
      email:
        recipients:
          - your-email@example.com
```

---

## 📱 یا سادہ تر:

### Project Structure:
```
avicenna-health/
├── mobile/          ← یہاں pubspec.yaml ہے!
│   ├── lib/
│   ├── pubspec.yaml
│   └── android/
└── codemagic.yaml   ← اگر اوپر والا نہیں کام کرے
```

---

## 🎯 Quick Fix Steps:

1. **Codemagic Dashboard** اونجا
2. **avicenna-health** app
3. **Settings → Build**
4. **Project root path: `mobile`**
5. **Save**
6. **Start new build**

---

## ✅ اگر پھر بھی خطا ہو:

### codemagic.yaml upload کرو:

```bash
cd c:\Project\AvicennaAI

# Create file
echo 'workflows:
  avicenna-health:
    name: Build APK
    environment:
      android_signing: 
        - avicenna_health_key
    scripts:
      - name: Get dependencies
        script: cd mobile && flutter pub get
      - name: Build APK
        script: cd mobile && flutter build apk --debug
    artifacts:
      - mobile/build/app/outputs/flutter-apk/app-debug.apk' > codemagic.yaml

# Push
git add codemagic.yaml
git commit -m "Add Codemagic configuration"
git push
```

---

## 🚀 پھر Codemagic میں:

1. **Rebuild**
2. APK build ہوگا! ✓

---

**کونسا حل آزمائیں؟**
