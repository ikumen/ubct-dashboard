import logging
import functools

from flask import Blueprint, request
from werkzeug.exceptions import Unauthorized, NotFound
from backend.helpers import route, try_parse_int
from backend.services import slackemoji_service, slackfile_service, slackmessage_service, slackuser_service, app_service, slackchannel_service


logger = logging.getLogger(__name__)
bp = Blueprint('api', __name__, url_prefix='/api/resource')


def authorized(func):
    """Decorator that checks for authorization header before calling wrapped function.
    """
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        auth_token = request.headers.get('Authorization', None)
        if not auth_token or not app_service.authorize(auth_token):
            raise Unauthorized('Not Authorized!')
        return func(*args, **kwargs)
    return decorator


def pageable(func):
    """Decorator that help populates the wrapped function with pagination 
    parameters, parsed from the request args.
    """
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        per_page = try_parse_int(request.args.get('per_page'), 50)
        page = try_parse_int(request.args.get('page'), 1)
        kwargs['per_page'] = per_page if 10 <= per_page <= 50 else 50
        kwargs['page'] = page if page > 0 else 1
        return func(*args, **kwargs)
    return decorator


def sortable(func):
    """Decorator that helps populate the wrapped function with sort parameters,
    parsed from the request args.
    """
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        if 'sort' in request.args:
            rv = request.args.get('sort').split(',')
            kwargs['sort'] = rv[0]
            kwargs['sort_dir'] = rv[1] if len(rv) == 2 else 'asc'
        return func(*args, **kwargs)
    return decorator


@route(bp, '/slack/users', methods=['get'])
@authorized
@sortable 
@pageable
def list_users(page, per_page, sort=None, sort_dir=None):
    filters = {}
    if 'tz_offset' in request.args:
        filters['tz_offset'] = request.args.get('tz_offset')
    return slackuser_service.find_all_with_paging(
        page=page, 
        per_page=per_page, 
        sort=sort, 
        sort_dir=sort_dir, 
        **filters
    )


@route(bp, '/slack/channels', methods=['get'])
@authorized
@sortable
@pageable
def list_channels(page, per_page, sort=None, sort_dir=None):
    return slackchannel_service.find_all_with_paging(
        page=page, 
        per_page=per_page, 
        sort=sort, 
        sort_dir=sort_dir
    )


@route(bp, '/slack/emojis', methods=['get'])
@authorized
@sortable
@pageable
def list_emojis(page, per_page, sort=None, sort_dir=None):
    return slackemoji_service.find_all_with_paging(
        page=page, 
        per_page=per_page, 
        sort=sort, 
        sort_dir=sort_dir
    )


@route(bp, '/slack/files', methods=['get'])
@authorized
@sortable
@pageable
def list_files(page, per_page, sort=None, sort_dir=None):
    filters = {}
    if 'channel_id' in request.args:
        filters['channel_id'] = request.args.get('channel_id')
    if 'message_id' in request.args:
        filters['message_id'] = request.args.get('message_id')
    return slackfile_service.find_all_with_paging(
        page=page, 
        per_page=per_page,
        sort=sort,
        sort_dir=sort_dir, 
        **filters
    )


@route(bp, '/slack/messages/<ch_id>/<msg_id>', methods=['get'])
@authorized
def get_message(ch_id, msg_id):
    message = slackmessage_service.get_by_id(ch_id, msg_id)
    if not message:
        raise NotFound
    return message


@route(bp, '/slack/messages', methods=['get'])
@authorized
@sortable
@pageable
def list_messages(page, per_page, sort=None, sort_dir=None):
    filters = {}
    if 'user_id' in request.args:
        filters['user_id'] = request.args.get('user_id')
    if 'channel_id' in request.args:
        filters['channel_id'] = request.args.get('channel_id')
    if 'thread_id' in request.args:
        filters['thread_id'] = request.args.get('thread_id')
    return slackmessage_service.find_all_with_paging(
        page=page, 
        per_page=per_page,
        sort=sort,
        sort_dir=sort_dir,
        **filters
    )