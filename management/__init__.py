def create_app():
    from flask import Flask
    from flask_cors import CORS
    from apps.middleware import cache, compress, jwt, swagger
    from core.config import redis_host, ENV
    import logging
    app = Flask(__name__)
    if ENV == 'LIVE':
        logging.info('we can not open our api server for live!!')
    else:
        app.config['SWAGGER'] = {
            "headers": [
                ('X-Client-Geo-Location', 'all'),
            ],
            "info": {
                'title': 'NET API DOCUMENT',
                'description': 'api server',
                'uiversion': 3,
                'version': '1.5.1'
            }
        }
        swagger.init_app(app)

    app.config["CACHE_TYPE"] = "redis"
    app.config["COMPRESS_REGISTER"] = False
    app.config["CACHE_REDIS_URL"] = redis_host
    app.config["MAX_CONTENT_LENGTH"] = 8 * 1024 * 1024
    # app.config['JWT_SECRET_KEY'] = jwt_options['secret_key']
    # app.config['JWT_TOKEN_LOCATION'] = jwt_options['jwt_token_location']
    # app.config['JWT_CSRF_METHODS'] = jwt_options['jwt_csrf_methods']
    # app.config['JWT_ACCESS_TOKEN_EXPIRES'] = jwt_options['jwt_access_token_expires']
    # app.config['JWT_REFRESH_TOKEN_EXPIRES'] = jwt_options['jwt_refresh_token_expires']
    # app.config['JWT_ACCESS_COOKIE_NAME'] = jwt_options['jwt_access_cookie_name']
    # app.config['JWT_REFRESH_COOKIE_NAME'] = jwt_options['jwt_refresh_cookie_name']
    # app.config['JWT_ACCESS_CSRF_COOKIE_NAME'] = jwt_options['jwt_access_csrf_cookie_name']
    # app.config['JWT_REFRESH_CSRF_COOKIE_NAME'] = jwt_options['jwt_refresh_csrf_cookie_name']

    CORS(app)
    cache.init_app(app)
    compress.init_app(app)
    jwt.init_app(app)

    from apps import main_page_api, admin_api, vuln_api, outage_api, detail_api
    app.register_blueprint(main_page_api)
    app.register_blueprint(admin_api)
    app.register_blueprint(vuln_api)
    app.register_blueprint(outage_api)
    app.register_blueprint(detail_api)
    return app
