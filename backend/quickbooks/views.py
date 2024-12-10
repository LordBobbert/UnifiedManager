# File: backend/quickbooks/views.py

from django.http import JsonResponse
from django.shortcuts import redirect
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .auth import get_authorization_url, exchange_code_for_tokens
from .models import QuickBooksToken
from .utils import fetch_quickbooks_customer_list, sync_client_to_quickbooks
from users.models import Client, Trainer

class QuickBooksLoginView(APIView):
    """
    Redirects the user to QuickBooks' OAuth2 login page.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return redirect(get_authorization_url())


class QuickBooksCallbackView(APIView):
    """
    Handles QuickBooks' OAuth2 callback, exchanges the code for tokens, and stores them.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        code = request.GET.get("code")
        if not code:
            return JsonResponse({"error": "Authorization code is missing."}, status=400)

        try:
            tokens = exchange_code_for_tokens(code)
            QuickBooksToken.objects.update_or_create(
                user=request.user,
                defaults={
                    "access_token": tokens["access_token"],
                    "refresh_token": tokens["refresh_token"],
                    "realm_id": tokens["realm_id"],
                    "expires_at": tokens["expires_at"],
                },
            )
            return JsonResponse({"message": "QuickBooks connected successfully."})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


class FetchQuickBooksCustomersView(APIView):
    """
    Fetch customers from QuickBooks Online and return them as JSON.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            qb_token = QuickBooksToken.objects.get(user=request.user)
            customers = fetch_quickbooks_customer_list(
                access_token=qb_token.access_token,
                realm_id=qb_token.realm_id,
            )
            return JsonResponse({"customers": customers}, safe=False)
        except QuickBooksToken.DoesNotExist:
            return JsonResponse({"error": "No QuickBooks token found for the user."}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


class SyncClientsToQuickBooksView(APIView):
    """
    Sync all clients to QuickBooks Online as customers.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            qb_token = QuickBooksToken.objects.get(user=request.user)
            clients = Client.objects.all()
            results = []

            for client in clients:
                qb_id = sync_client_to_quickbooks(
                    client=client,
                    access_token=qb_token.access_token,
                    realm_id=qb_token.realm_id,
                )
                results.append({"client_id": client.id, "quickbooks_id": qb_id})

            return JsonResponse({"synced": results})
        except QuickBooksToken.DoesNotExist:
            return JsonResponse({"error": "No QuickBooks token found for the user."}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

class SyncTrainersToQuickBooksView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            qb_token = QuickBooksToken.objects.get(user=request.user)
            trainers = Trainer.objects.all()  # Assuming a Trainer model exists
            results = []

            for trainer in trainers:
                qb_id = sync_client_to_quickbooks(
                    client=trainer,  # Use same function for trainers
                    access_token=qb_token.access_token,
                    realm_id=qb_token.realm_id,
                )
                results.append({"trainer_id": trainer.id, "quickbooks_id": qb_id})

            return JsonResponse({"synced": results})
        except QuickBooksToken.DoesNotExist:
            return JsonResponse({"error": "No QuickBooks token found for the user."}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
