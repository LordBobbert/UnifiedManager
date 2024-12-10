# File: backend/quickbooks/auth.py

from intuitlib.client import AuthClient
from intuitlib.exceptions import AuthClientError
from django.conf import settings

auth_client = AuthClient(
    client_id=settings.QUICKBOOKS_CLIENT_ID,
    client_secret=settings.QUICKBOOKS_CLIENT_SECRET,
    environment=settings.QUICKBOOKS_ENVIRONMENT,
    redirect_uri=settings.QUICKBOOKS_REDIRECT_URI,
)

def get_authorization_url():
    """
    Generate the QuickBooks authorization URL.
    """
    return auth_client.get_authorization_url(scopes=["com.intuit.quickbooks.accounting"])

def exchange_code_for_tokens(auth_code):
    """
    Exchange the authorization code for an access token.
    """
    try:
        auth_client.get_bearer_token(auth_code)
        return {
            "access_token": auth_client.access_token,
            "refresh_token": auth_client.refresh_token,
            "realm_id": auth_client.realm_id,
            "expires_at": auth_client.expires_at,
        }
    except AuthClientError as e:
        raise Exception(f"Failed to fetch tokens: {str(e)}")
