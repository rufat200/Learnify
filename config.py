import os

from dotenv import load_dotenv


load_dotenv()


SECRET_KEY = os.getenv("SECRET_KEY", "secret key")
DEBUG = bool(os.getenv("DEBUG", False))
ALLOWED_HOSTS = [os.getenv("ALLOWED_HOSTS", "*")]

ENGINE = os.getenv("DB_ENGINE")
NAME = os.getenv("DB_NAME")
USER= os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")
HOST = os.getenv("DB_HOST")
PORT = os.getenv("DB_PORT")

EMAIL_BACKEND = os.getenv("EMAIL_BACKEND")
SMTP_HOST = os.getenv("EMAIL_HOST")
SMTP_PORT = os.getenv("EMAIL_PORT")
SMTP_USE_TLS = bool(os.getenv("EMAIL_USE_TLS", False))
SMTP_HOST_USER = os.getenv("EMAIL_HOST_USER")
SMTP_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")