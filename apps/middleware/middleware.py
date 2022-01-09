from flask_caching import Cache
from flask_compress import Compress
from flask_jwt_extended import JWTManager
from azure.storage.blob import BlockBlobService
from core.config import azure_options
from flasgger import Swagger


swagger = Swagger()
jwt = JWTManager()
cache = Cache()
compress = Compress()

blob_service = BlockBlobService(account_name=azure_options['account_name'], account_key=azure_options['account_key'])
