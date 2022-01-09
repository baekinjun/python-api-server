import socket
import yaml

HOST_NAME = socket.gethostname()

if HOST_NAME == "LiVE":
    ENV = 'LIVE'
else:
    ENV = 'TEST'

with open('core/config.yml') as f:
    settings = yaml.load(f, Loader=yaml.Loader)
    common_settings = settings['common']
    env_settings = settings[ENV]
    jwt_options = settings['JWT']
    azure_options = settings['AZURE_STORAGE']

APP = common_settings['APP']
fake_key = common_settings['fake_key']
API_KEY = common_settings['API_KEY']

redis_host = env_settings['redis']['host']
G_DATABASE = env_settings['G_DATABASE']

