from apps.admin_api.controller import *

url_patterns = [
    (DescriptionView, '/description'),
    (UDescriptionView, '/descriptionU'),
    (DDescriptionView, '/descriptionD'),
    (RegistartionView, '/registration'),
    (URegistartionView, '/registrationU'),
    (DRegistartionView, '/registrationD'),
    (HomePageListView, '/homepagelist'),
    (ApiListView, '/apilist'),
    (SearchKeywordListView, '/search-keyword-list'),
    (NewsDataView, '/news-data')
]
