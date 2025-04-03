from django.shortcuts import redirect
from rest_framework.authtoken.models import Token
from django.contrib.auth.decorators import login_required
from allauth.socialaccount.models import SocialToken, SocialAccount

@login_required
def google_auth_callback(request):
    try:
        redirect_uri = request.GET.get("next", "/")
        social_account = SocialAccount.objects.get(user = request.user)
        social_token = SocialToken.objects.get(account = social_account, account__provider = "google")
        token, _ = Token.objects.get_or_create(user=request.user)
        return redirect(f"http://localhost:5173/learn")
    
    except SocialAccount.DoesNotExist:
        return redirect(f"{redirect_uri}?error=No Google account found")
    except:
        return redirect(f"{redirect_uri}?error=Internal server error")