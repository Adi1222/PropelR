from PropelRapp.models import *
from django.contrib.auth.models import User

def appuser(request):
    assert hasattr(request,'user')

    if request.user == 'Anonymoususer':
        pass
    #appuser = Appuser.objects.get(created_by=request.user.username)
    return {'appusers': Appuser.objects.all()}


def roles(request):
    return {'roles' : Role.objects.all()}


def roledetail(request):
        return {'roledetails': Roledetail.objects.all()}


def menus(request):
    return {'menus': Menu.objects.all()}


def submenus(request):
    return {'submenus': Submenu.objects.all()}