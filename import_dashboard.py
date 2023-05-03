import requests.adapters
import requests.exceptions
import requests_oauthlib
import urllib.parse
from os import path, getenv

def login_superset():
    """
    Generate a session for interacting with Superset

    Returns: Login token (Bearer) and Session object
    """
    print('Start Superset authentication')
    # Login
    login_endpoint = urllib.parse.urljoin(URL_BASE, '/api/v1/security/login')
    response = requests.post(
        login_endpoint,
        json={
            "username": getenv('SUPERSET_USERNAME'),
            "password": getenv('SUPERSET_PASSWORD'),
            "provider": 'db',
            "refresh": "true",
        },
    )

    login_token = response.json()

    # Create session
    session = requests_oauthlib.OAuth2Session(token=login_token)
    print('Session created successfully')
    return login_token, session

def get_csrf_token(session):
    """
    Use Superset API to retrieve the CSRF token for this session
    
    Arguments:
        session -- Session object used for the API request
    
    Returns: CSRF token
    """
    print('Start request to retrieve CSRF token')
    # Get CSRF Token
    csrf_endpoint = urllib.parse.urljoin(URL_BASE, '/api/v1/security/csrf_token/')
    headers={"Referer": csrf_endpoint}
    csrf_response = session.get(
        url=csrf_endpoint,
        headers=headers
    )
    csrf_token = csrf_response.json().get("result")
    print('CSRF token received succesfully')
    return csrf_token

def import_dashboard(session, login_token, csrf_token):
    """
    Import a dashboard from the specified output path to Superset

    Arguments:
        session -- Session object used for the API request
        login_token -- Bearer token for the API request
        csrf_token -- CSRF token for the API request
    """
    container_dashboard_path = path.join('/', 'github', 'workspace', DASHBOARD_FILE_PATH)
    print(f'Start importing the dashboard from {container_dashboard_path}')
    # Import dashboard
    import_endpoint = urllib.parse.urljoin(URL_BASE, '/api/v1/dashboard/import/')

    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {login_token}',
        'X-CSRFToken': csrf_token,
        'Referer': import_endpoint
    }

    files = { 
    'formData': (
        container_dashboard_path, 
        open(container_dashboard_path, 'rb'), 
        'application/json'
        )
    }

    payload = {"overwrite":'true'}

    response = session.post(
                url=import_endpoint, 
                headers=headers,
                files=files,
                data=payload
        )
    assert response.status_code == 200, f'Error in importing the dashboard\n{response}'
    print(f'Dashboard imported succesfully from {container_dashboard_path}')

def main():
    login_token, session = login_superset()
    csrf_token = get_csrf_token(session)
    import_dashboard(session, login_token, csrf_token)

if __name__ == '__main__':
    URL_BASE = getenv('INPUT_URL_BASE', 'http://localhost:8088')
    DASHBOARD_FILE_PATH = getenv('INPUT_DASHBOARD_FILE_PATH')
    main()