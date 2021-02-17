import logging
import secrets

from flask import Blueprint, render_template, session, redirect, request, jsonify, current_app
from werkzeug.exceptions import NotFound
from backend import auth
from backend.services import app_service, storage_service, user_service, \
    slackchannel_service, slackemoji_service, slackuser_service, \
    slackreaction_service, slackmessage_service, slackfile_service, cache


logger = logging.getLogger(__name__)
bp = Blueprint('web', __name__,  
    url_prefix='/',
    template_folder='../frontend/public', 
    static_url_path='/static',
    static_folder='../frontend/public/static'
)

template_spa = 'index.html'

# Url constants
url_spa_entry = '/'
url_spa_verify = '/verify'
url_spa_user = '/user'

url_api_user_apps = '/api/user/apps'
url_api_user = '/api/user'


@bp.route(url_api_user_apps, methods=['post'])
@auth.authenticated
def register_app(user):
    data = request.get_json()
    app = app_service.create(
        **data, 
        user_id=user['id'], 
        token=secrets.token_urlsafe(32)
    )
    return jsonify(app), 201


@bp.route(url_api_user_apps, methods=['get'])
@auth.authenticated
def list_apps(user):
    apps = app_service.all_by_user(user['id'])
    return jsonify(apps), 200


@bp.route(f'{url_api_user_apps}/<id>', methods=['delete'])
@auth.authenticated
def delete_app(id, user):
    app = app_service.soft_delete_by_user(id, user['id'])
    return jsonify(app), 200


@bp.route(url_api_user, methods=['delete'])
@auth.authenticated
def delete_user(user):
    user_service.soft_delete(user['id'])
    return jsonify(user), 200


@bp.route(url_spa_verify)
@auth.authenticated_unverified
def view_verify(user):
    """Return the verify user view.
    """
    if user.get(auth.key_is_verified):
        return redirect(url_spa_user)
    return render_template(template_spa)


@bp.route(url_spa_user)
@auth.authenticated
def view_user(user):
    """Return the user view.
    """
    if not user.get(auth.key_is_verified):
        return redirect(url_spa_verify)
    return render_template(template_spa)


@bp.route('/user')
@auth.authenticated
def view_user_profile(user):
    return render_template(template_spa)


@bp.route('/data')
@auth.authenticated
def view_data(user):
    return render_template(template_spa)


@cache.cached(timeout=7200) # 2hrs
def _get_dataset_stats():
    return dict(counts=dict(
        channels=slackchannel_service.count(),
        users=slackuser_service.count(),
        messages=slackmessage_service.count(),
        files=slackfile_service.count(),
        emojis=slackemoji_service.count(),
        reactions=slackreaction_service.count()
    ))


@bp.route('/api/datasets')
@auth.authenticated
def view_datasets(user):
    return dict(
        stats=_get_dataset_stats(),
        datasets=storage_service.list_dataset_container_files()
    ), 200


@bp.route('/dataset')
@auth.authenticated
def view_dataset_file(user):
    f = request.args.get('f')
    if not f or f not in [d['name'] for d in storage_service.list_dataset_container_files()]:
        raise NotFound
    return redirect(storage_service.get_url_for_dataset_file(f))


@bp.route('/help')
def view_help():
    return render_template(template_spa)


@bp.route(url_spa_entry)
def view_home():
    """Return home page.
    """
    if auth.key_auth_user in session:
        if session[auth.key_auth_user].get(auth.key_is_verified):
            return redirect(url_spa_user)
        return redirect(url_spa_verify)
    return render_template(template_spa)


