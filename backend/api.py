import logging
import functools

from flask import Blueprint, request
from werkzeug.exceptions import Unauthorized
from backend.helpers import route, try_parse_int
from backend.services import slackuser_service, app_service, slackchannel_service


logger = logging.getLogger(__name__)
bp = Blueprint('api', __name__, url_prefix='/api/resource')


def authorized(func):
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        auth_token = request.headers.get('Authorization', None)
        if not auth_token or not app_service.authorize(auth_token):
            raise Unauthorized('Not Authorized!')
        return func(*args, **kwargs)
    return decorator


def pageable(func):
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        per_page = try_parse_int(request.args.get('per_page'), 100)
        page = try_parse_int(request.args.get('page'), 1)
        kwargs['per_page'] = per_page if 10 <= per_page <= 100 else 10
        kwargs['page'] = page if page > 0 else 1
        return func(*args, **kwargs)
    return decorator


@route(bp, '/slack/users', methods=['get'])
@authorized
@pageable
def list_users(page, per_page):
    filters = {}
    tz_offset_filter = request.args.get('tz_offset')
    if tz_offset_filter:
        filters['tz_offset'] = tz_offset_filter
    return slackuser_service.find_all_with_paging(page=page, per_page=per_page, **filters)


@route(bp, '/slack/channels', methods=['get'])
@authorized
@pageable
def list_channels(page, per_page):
    return slackchannel_service.find_all_with_paging(page=page, per_page=per_page)
