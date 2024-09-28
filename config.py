import os

class Config:
    SECRET_KEY = 'your-secret-key-here'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'app', 'static', 'uploads')
    ADMIN_USERNAME = 'Milo123'
    ADMIN_PASSWORD = 'Milopilo0811'
    DISCORD_WEBHOOK_URL = 'https://discord.com/api/webhooks/1288968695686627358/I9uNFI_pNYH9w0jmY5Cic4VfxOzB2pfyJn3WyzELSd5huonVyOPUjn_YXH5qtG1UT8Kq'