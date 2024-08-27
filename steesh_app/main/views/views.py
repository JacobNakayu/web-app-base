import re
import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
# from main.utils import getRecentNew

from users.models import User
from main.models import Ticket, Vulnerability

# from users.decorators import CAS_login_required, user_required, admin_required
# from main.servicenow import getServiceNowLink, getSysId

# Home page just to start off with. Later, mabybe add graphs and whatnot?
# Authentication wrappers
def homepage(request):
    return render(
        request,
        "vite_build/index.html"
    )
