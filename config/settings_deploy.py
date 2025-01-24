from pathlib import Path
import platform

# Build paths inside the project like this:
# BASE_DIR / 'subdir'
BASE_DIR = Path(__file__).resolve().parent.parent

# Build local paths like this: BASE_DIR / 'subdir'
# BASE_DIR / 'subdir' = './subdir'
RESULT_LOCAL_FOLDER = BASE_DIR / 'RESULT'
# WARNING_FOLDER = BASE_DIR / 'WARNING'

# Connection settings for SHARE
SHARE = 'UPR_6/IP-FINDER'
SHARE_LOG = 'LOGS'
SHARE_REQUEST = 'REQUESTS'
SHARE_WARNING = 'WARNING_NUMBERS'
SHARE_HOST = ''
SHARE_USERNAME = ''
SHARE_PASSWORD = ''

# Network folder and mount point based on OS
if platform.system() == "Linux":  # Linux
    LOG_FOLDER = f'//{SHARE_HOST}/{SHARE}/{SHARE_LOG}'
    MOUNT_POINT_LOG = Path('/mnt/log_folder')
    REQUEST_FOLDER = f'//{SHARE_HOST}/{SHARE}/{SHARE_REQUEST}'
    MOUNT_POINT_REQUEST = Path('/mnt/request_folder')
    WARNING_FOLDER = f'//{SHARE_HOST}/{SHARE}/{SHARE_WARNING}'
    MOUNT_POINT_WARNING = Path('/mnt/warning_folder')
elif platform.system() == "Darwin":  # macOS
    LOG_FOLDER = f'smb://{SHARE_USERNAME}:{SHARE_PASSWORD}@{SHARE_HOST}/{SHARE}/{SHARE_LOG}'
    MOUNT_POINT_LOG = Path('~/mnt/log_folder').expanduser()
    REQUEST_FOLDER = f'smb://{SHARE_USERNAME}:{SHARE_PASSWORD}@{SHARE_HOST}/{SHARE}/{SHARE_REQUEST}'
    MOUNT_POINT_REQUEST = Path('~/mnt/request_folder').expanduser()
    WARNING_FOLDER = f'smb://{SHARE_USERNAME}:{SHARE_PASSWORD}@{SHARE_HOST}/{SHARE}/{SHARE_WARNING}'
    MOUNT_POINT_WARNING = Path('~/mnt/warning_folder').expanduser()
else:
    raise OSError("Unsupported operating system. Only macOS and Linux are supported.")

USERNAME = ''

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
    'filter': {
        'ENGINE': 'dj_db_conn_pool.backends.oracle',
        'POOL_OPTIONS': {
            'POOL_SIZE': 5,
            'MAX_OVERFLOW': 5},
        'HOST': '',
        'PORT': '',
        'NAME': '',
        'USER': '',
        'PASSWORD': ''
    },
    'auth': {
        'ENGINE': 'django.db.backends.oracle',
        'HOST': '',
        'PORT': '',
        'NAME': '',
        'USER': '',
        'PASSWORD': ''
    }
}

OPERATORS = {
    '3Mob': '3MOB',
    'Vodafone': 'MTS',
    'UMC': 'MTS',
    'MTS': 'MTS',
    'VF-Ukraine': 'MTS',
    'VF UKRAINE': 'MTS',
    'KS': 'KS',
    'Kyivstar': 'KS',
    'Kyivstar UA': 'KS',
    'Kievstar': 'KS',
    'Kievstar GSM': 'KS',
    'lifecell': 'LIFE',
    'Lifecell': 'LIFE',
    'LifeCell': 'LIFE',
    'life': 'LIFE',
    'LIFE': 'LIFE',
    'LIFECELL': 'LIFE',
    'life:)': 'LIFE'
}

MOB3_IPS = ()
MTS_IPS = ('46.133', '89.209', '31.144', '128.124', '178.133')
# KS_IPS = ('46.211', '94.153.112')
KS_IPS = ('46.211', '94.153', '5.248')
LIFE_IPS = ('37.73', '46.96', '88.154', '88.155')

# MOB3_INNER_IPS = (10, 37, 192)
# MTS_INNER_IPS = (10, 11, 100, 192)
# KS_INNER_IPS = (10, 11, 100, 111, 134, 188, 192, '2a02')
# LIFE_INNER_IPS = (10, 11, 100, 192)

ORACLE_FUNCTIONS = {
    # 'tel_func': 'NEVA.ip_tr.restore_tel_from_ip_list',
    'tel_func': 'NEVA.ip_tr.get_ip_list',
    # 'inner_tel_func': 'NEVA.ip_tr.restore_tel_from_inner_ip_list',
    'inner_tel_func': 'NEVA.ip_tr.get_inner_ip_list',
    'check_tel_func': 'NEVA.ip_tr.check_tel',
    'check_login_proc': 'check_login'
}
