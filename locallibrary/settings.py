# locallibrary/settings.py

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# ==================== 基本設定 ====================

SECRET_KEY = "django-insecure-hwzwl3x&0c9g*nkyisq50*ffl4f-9yjlwq=6=dj$$il!t!1v@b"

DEBUG = True

ALLOWED_HOSTS = []   # 之後如果要部屬到雲端，再加網域或 IP 即可［web:111］


# ==================== App 註冊 ====================

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "catalog",  # 你的成績系統 app
]


# ==================== Middleware ====================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",  # 處理登入狀態［web:108］
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "locallibrary.urls"


# ==================== Templates ====================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "locallibrary.wsgi.application"


# ==================== 資料庫 ====================

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# ==================== 密碼規則 ====================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 8},   # 至少 8 碼，對學生比較安全［web:115］
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# ==================== 語系與時間 ====================

LANGUAGE_CODE = "zh-hant"

TIME_ZONE = "Asia/Taipei"   # 改成台灣時區，比 UTC 更直覺［web:115］

USE_I18N = True

USE_TZ = True


# ==================== 靜態檔案 ====================

STATIC_URL = "static/"

# 可以之後再加 STATICFILES_DIRS / STATIC_ROOT 做 CSS/圖片收集［web:109］


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
