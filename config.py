import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'nusantarakos-secret-key-2026'
    MYSQL_HOST = os.environ.get('MYSQL_HOST') or 'zokekf.h.filess.io'
    _port_raw = os.environ.get('MYSQL_PORT', '').strip()
    MYSQL_PORT = int(_port_raw) if _port_raw.isdigit() else 3307
    MYSQL_USER = os.environ.get('MYSQL_USER') or 'db_nusakost_upelevenhe'
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD') or 'd270fe84ac85a436959625052e126cd1a597ccdd'
    MYSQL_DB = os.environ.get('MYSQL_DB') or 'db_nusakost_upelevenhe'
    # Vercel has a read-only filesystem; use /tmp as writable fallback for uploads
    _base_dir = os.path.abspath(os.path.dirname(__file__))
    _local_upload = os.path.join(_base_dir, 'static', 'uploads')
    UPLOAD_FOLDER = '/tmp/uploads' if os.environ.get('VERCEL') else _local_upload
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max limit
