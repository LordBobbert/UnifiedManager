# File: backend/quickbooks/utils.py

import requests

from quickbooks.objects.customer import Customer
from quickbooks import QuickBooks

def fetch_quickbooks_customer(access_token, realm_id, customer_id):
    """
    Fetch customer data from QuickBooks Online.
    """
    url = f"https://sandbox-quickbooks.api.intuit.com/v3/company/{realm_id}/customer/{customer_id}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json",
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def fetch_quickbooks_customer_list(access_token, realm_id):
    """
    Fetch the list of all customers from QuickBooks Online.
    """
    url = f"https://sandbox-quickbooks.api.intuit.com/v3/company/{realm_id}/query"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json",
    }
    query = "SELECT * FROM Customer"
    response = requests.get(f"{url}?query={query}", headers=headers)
    response.raise_for_status()
    return response.json().get('QueryResponse', {}).get('Customer', [])

def sync_client_to_quickbooks(client, access_token, realm_id):
    """
    Sync a client's data to QuickBooks Online as a Customer.
    """
    qb_client = QuickBooks(
        sandbox=True,  # Set to False for production
        client_id=settings.QUICKBOOKS_CLIENT_ID,
        client_secret=settings.QUICKBOOKS_CLIENT_SECRET,
        access_token=access_token,
        company_id=realm_id,
    )

    qb_customer = Customer()
    qb_customer.DisplayName = f"{client.first_name} {client.last_name}"
    qb_customer.PrimaryEmailAddr = {"Address": client.email}
    qb_customer.PrimaryPhone = {"FreeFormNumber": client.phone}
    qb_customer.BillAddr = {
        "Line1": client.address_line1,
        "City": client.city,
        "Country": client.country,
        "PostalCode": client.postal_code,
    }

    # Save the customer to QuickBooks
    qb_customer.save(qb_client)
    return qb_customer.Id