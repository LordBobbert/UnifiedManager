from django.urls import path
from .views import (
    QuickBooksLoginView,
    QuickBooksCallbackView,
    FetchQuickBooksCustomersView,
    SyncClientsToQuickBooksView,
)

urlpatterns = [
    path('login/', QuickBooksLoginView.as_view(), name='quickbooks-login'),
    path('callback/', QuickBooksCallbackView.as_view(), name='quickbooks-callback'),
    path('customers/fetch/', FetchQuickBooksCustomersView.as_view(), name='fetch-customers'),
    path('clients/sync/', SyncClientsToQuickBooksView.as_view(), name='sync-clients'),
]
