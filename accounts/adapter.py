from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter
from django.contrib.auth import get_user_model
from allauth.account.utils import get_next_redirect_url
User = get_user_model()
class CorporateAdapter(DefaultAccountAdapter):
	# def get_login_redirect_url(self, request):
	#	 path = "/results/{username}/"
	#	 return path.format(username=request.user.username)
	def get_login_redirect_url(self, request, **kwargs):
		userr = User.objects.get(username=request.user)
		userr_profile = userr.get_user_profile()
		threshold = 10
		if userr.corporate ==False:
			return '/profile/update/'
			
		else:
			return '/corporate/results/'
	def print_keyword_args(kwargs):
		# kwargs is a dict of the keyword args passed to the function
		for key, value in kwargs.iteritems():
			print "%s = %s" % (key, value)