# Override the database settings for GitHub Actions
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "github_actions",
        "USER": "metalbrain",
        "PASSWORD": "postgres",
        "HOST": "db",
        "PORT": "5432",
    }
}
