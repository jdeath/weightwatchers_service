import requests
from datetime import date
import logging

DOMAIN = "weightwatchers_service"
ATTR_NAME = "weight"
DEFAULT_NAME = "None"
UNITS = "lbs"
USERNAME = "XXXX"
PASSWORD = "XXXX"

_LOGGER = logging.getLogger(__name__)

def setup(hass, config):
    """Set up is called when Home Assistant is loading our component."""

    def handle_weightwatchers(call):
        """Handle the service call."""
        weight = call.data.get(ATTR_NAME, DEFAULT_NAME)
        _LOGGER.debug("Weight: " + str(weight))
        
        if weight != DEFAULT_NAME:
            _setWeight(weight)

    hass.services.register(DOMAIN, "set_weight", handle_weightwatchers)

    # Return boolean to indicate that initialization was successful.
    return True
    
def _setWeight(weight):
    headers = {
    'Authorization': 'Basic YW5kcm9pZEF1dGg6dzVucUlhNHRFL0tJa0pvNnBNRDJ2cmRUalBnVzRxQTJqRC9OVnUwaHg1YWtHcDhiaUNMQUE3bG9HcDFlSk9MUQ==',
    'Accept': '*/*',
    'Accept-Language': 'en-US',
    'Referer': 'WW_Mobile',
    'X-SessionId': '68fc519a-0de7-4fe3-b88b-fa97d1b3ee30',
    'x-client-timestamp': '2023-01-31T21:15:36.692-0500',
    'User-Agent': 'WWApp WWMobile/10.30.0 (Android/12; Google sdk_gphone64_x86_64)',
    'Host': 'auth.weightwatchers.com',
    'Connection': 'Keep-Alive',
    }

    data = {
        'grant_type': 'password',
        'username': USERNAME,
        'password': PASSWORD,
        'scope': 'openid profile',
    }
    s = requests.Session()

    response = s.post('https://auth.weightwatchers.com/openam/oauth2/access_token', headers=headers, data=data)
    _LOGGER.debug(response.json())
    responseJSON = response.json()

    #session_token = responseJSON.get('session_token')
    #refresh_token = responseJSON.get('refresh_token')
    #expires_in = responseJSON.get('expires_in')

    id_token = responseJSON.get('id_token')
    _LOGGER.debug("id_token: " + id_token)
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-US',
        'Referer': 'WW_Mobile',
        'X-SessionId': '68fc519a-0de7-4fe3-b88b-fa97d1b3ee30',
        'x-client-timestamp': '2023-01-31T21:16:26.570-0500',
        'User-Agent': 'WWApp WWMobile/10.30.0 (Android/12; Google sdk_gphone64_x86_64)',
        'Authorization': 'Bearer ' + id_token,
        'Content-Type': 'application/json; charset=UTF-8',
        'Host': 'cmx.weightwatchers.com',
        'Connection': 'Keep-Alive',
    }

    json_data = {
        'source': '',
        'notes': 'Updated by Homeassistant',
        'weighDate': str(date.today()),
        'weight': weight,
        'units': UNITS,
    }
    _LOGGER.debug(json_data)
    response = s.post(
        'https://cmx.weightwatchers.com/api/v1/cmx/members/~/weightEntries',
        headers=headers,
        json=json_data,
    )
    _LOGGER.debug(response.json())