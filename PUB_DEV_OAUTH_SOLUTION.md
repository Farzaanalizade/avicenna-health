# 🔧 راه حل: OAuth2 Token برای pub.dev

## مسئله:
- App Password (atuipwbibtoofsja) برای pub.dev OAuth2 **کار نمی‌کند**
- Dart pub نیاز به **OAuth2 Bearer Token** دارد، نه username/password

## راه حل:

### گام 1: Browser-Based Login
1. اجرا کنید:
```powershell
dart pub token add https://pub.dev
```

2. وقتی نوشت شد:
```
> Pub will open a browser to https://...
> Copy and paste this code into your browser: [CODE]
```

**شما باید:**
- Browser را بسازید
- گوگل 2FA کد را وارد کنید
- Authorization کنید
- Code رو کپی و paste کنید

### یا: استفاده از Pub.dev Website

1. رفتن به: https://pub.dev
2. Login with: saal2070@gmail.com (2FA code needed)
3. رفتن به: Settings → Credentials → Create New
4. Copy the token
5. ذخیره Token در: `C:\Users\[USERNAME]\.pub-cache\credentials.json`

```json
{
  "version": 1,
  "configHosts": {
    "https://pub.dev": {
      "hosted": {
        "url": "https://pub.dev"
      },
      "token": "[COPY_PASTE_TOKEN_HERE]"
    }
  }
}
```

## اگر به Browser Access ندارید:

شما باید برای من **OAuth2 token** (نه app password) فراهم کنید:

1. رفتن به: https://pub.dev/account/oauth-apps
2. Create new OAuth app (or use existing)
3. یا رفتن به Settings و copy کنید token

Token معمولاً شبیه این است:
```
glf-1234567890abcdefghijklmnopqrst
```
