import time

from django import template
from django.conf import settings
from django.utils import simplejson
from django.utils.hashcompat import sha_constructor

register = template.Library()

@register.inclusion_tag("intercom/_intercom_js.html")
def intercom_js(request):
	
	user = request.user
	
	if hasattr(settings, "INTERCOM_APP_ID") and user.is_authenticated():

		if hasattr(settings, "INTERCOM_USER_HASH_KEY") and user.email:

			user_hash = sha_constructor(settings.INTERCOM_USER_HASH_KEY + user.email).hexdigest()

		else:

			user_hash = None
			
		company = request.company
		
		custom_data = {
		
			'company_name' : company.company_name,
			
			'account_status' : company.account_status,
		
		}
		
		return {
			
			"app_id": settings.INTERCOM_APP_ID,
			
			"email": user.email,
			
			'user_id' : user.id,
			
			"user_hash": user_hash,
			
			"created_at": int(time.mktime(user.date_joined.timetuple())),
			
			"custom_data": simplejson.dumps(custom_data, ensure_ascii=False)
		}
		
	else:

		return {}