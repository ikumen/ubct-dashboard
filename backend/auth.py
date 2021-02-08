import functools
import logging
import re
import requests
import uuid

from datetime import datetime
from flask import Blueprint, session, redirect, current_app, request, url_for
from werkzeug.exceptions import Unauthorized, BadRequest, Forbidden

from backend import frontend
from backend.services import oauth_service, user_service


logger = logging.getLogger(__name__)
bp = Blueprint('auth', __name__)


url_signout = '/signout'

# Authenticated user
key_auth_user = 'auth_user'
key_is_verified = 'is_verified'
key_verify_nonce = 'nonce'
key_verify_expire_ts = 'expire_ts'

_oauth_plugins = {}


def __authenticated(func, *args, allow_unverified=False, **kwargs):
    user = session.get(key_auth_user)
    if user and (allow_unverified or user.get(key_is_verified)):
        return func(*args, user=user, **kwargs)
    if request.content_type == 'application/json':
        raise Unauthorized('Authorization is required')
    return redirect(url_signout)


def authenticated(func):
    """Decorator for routes that require an verified authenticated user,
    otherwise redirect to /signout.
    """
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        return __authenticated(func, *args, allow_unverified=False, **kwargs)
    return decorator


def authenticated_unverified(func):
    """Decorator for routes that require an unverified authenticated user,
    otherwise redirect to /signout.
    """
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        return __authenticated(func, *args, allow_unverified=True, **kwargs)
    return decorator


def register_signin_complete_handler(func):
    match = re.search('^(\S+)_signin_complete', func.__name__)
    if not match:
        raise NameError('Registered oauth handler name should be in format "<provider>_signin_complete"')
    _oauth_plugins[match.group(1)] = func
    return func


@register_signin_complete_handler
def azure_signin_complete(provider, oauth_client):
    """Handle successful Azure signins.
    """
    token = oauth_client.authorize_access_token()
    oa_user = oauth_service.azure.parse_id_token(token)
    name = oa_user['preferred_username']
    # Check for email (via @), then grab prefix (before @) as group 1
    email_match = re.search('^(\S+)@.+', name)
    if email_match:
        # Normalize the name to only email prefix, not full email
        logger.debug('Email normalized')
        name = email_match.group(1)
    return dict(
        oa_provider=provider,
        oa_id=oa_user['oid'],
        name=name)


@register_signin_complete_handler
def github_signin_complete(provider, oauth_client):
    """Handle successful GitHub signin.
    """
    token = oauth_client.authorize_access_token()
    oa_user = oauth_client.get('user').json()
    logger.debug(f'Github oa_user={oa_user}')
    return dict(
        oa_provider=provider,
        oa_id=str(oa_user['id']),
        name=oa_user['login'])


@bp.route('/signin/<provider>')
def signin(provider):
    """Start authorization for the requested provider.
    """
    logger.info(f'Trying to sign in for provider: {provider}')
    redirect_uri = url_for(f'.signin_complete', _external=True, provider=provider)
    return oauth_service.create_client(provider).authorize_redirect(redirect_uri)


@bp.route('/signin/<provider>/complete')
def signin_complete(provider):
    """Handle successful signins. Delegates extracting user info to OAuth 
    provider specific helper methods.
    """
    oa_user = _oauth_plugins[provider](provider, oauth_service.create_client(provider))
    user = user_service.find_by_oauth(oa_id=oa_user['oa_id'], oa_provider=provider)
    logger.debug(f'Signin complete: oa_user={oa_user}, user={user}')
    if user: 
        # user already exists, they are signin and good to go
        session[key_auth_user] = {
            **user.to_json(),
            key_is_verified: True
        }
        return redirect(frontend.url_spa_user)
    else:
        # first time, send them page to verify they are scholar
        oa_user[key_verify_expire_ts] = datetime.now().timestamp() + 1200 #20mins
        oa_user[key_verify_nonce] = str(uuid.uuid4())
        oa_user[key_is_verified] = False
        session[key_auth_user] = oa_user
        return redirect(frontend.url_spa_verify)


@bp.route('/api/auth/providers', methods=['get'])
def auth_providers():
    """Return list of OAuth provider ids and labels.
    """
    return current_app.config['OAUTH_PROVIDERS']


@bp.route(url_signout)
def signout():
    """Sign out (clear) current user session, then kick user to sign in url.
    """
    session.clear()
    return redirect(frontend.url_spa_entry)


def _is_valid_verify_session(user):
    """For users who require verification, we limit their session time. To
    validate if they have a valid session, check the given user (from session)
    is not None and has a start time that is less then xmins old.
    """
    return (user and user.get(key_verify_expire_ts) 
        and (user[key_verify_expire_ts] - datetime.now().timestamp() > 0))


def _is_valid_verify_url(url):
    valid_verify_url_regex = f'^https://slack-files.com/{current_app.config.get("SLACK_TEAM")}-'
    return url and re.search(valid_verify_url_regex, url)


@bp.route('/api/auth/verify')
def auth_verify():
    """Verify the user by checking if given verify url contains the 
    expected nonce we created for them earlier.
    """
    user = session.get(key_auth_user)
    if not _is_valid_verify_session(user):
        raise Unauthorized()

    verify_url = request.args.get('u')
    if not _is_valid_verify_url(verify_url):
        # https://slack-files.com/....-
        raise BadRequest(f'Invalid verify url: {verify_url}')

    verify_resp = requests.request('get', verify_url)
    if verify_resp.status_code != 200 or user[key_verify_nonce] not in verify_resp.text:
        raise BadRequest(f'Unable to verify token at Slack url: {verify_url}, {verify_resp.reason}')

    # User has passed verification, lets clear out the old session
    # and add them to the database, then set them up with new session
    # that has longer expire time.
    session.clear()
    created_user = user_service.create(
        oa_id=user['oa_id'],
        oa_provider=user['oa_provider'],
        name=user['name']
    )
    
    session[key_auth_user] = {
        **created_user.to_json(),
        key_is_verified: True
    }
        
    return session[key_auth_user], 200


@bp.route('/api/auth/user')
@authenticated_unverified
def current_user(user):
    return user
