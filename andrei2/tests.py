from django.test import TestCase

# Create your tests here.

def runtests():
    os.environ["DJANGO_SETTINGS_MODULE"] = "tests.settings"

    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()

    from django.core.management import call_command
    result = call_command('test', 'userapp')
    sys.exit(result) 