INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Var olan uygulamalar
    'users.apps.UsersConfig',
    'dietplan.apps.DietplanConfig',
    'home',

    # Yeni eklenen iletişim uygulaması
    'contact',
]