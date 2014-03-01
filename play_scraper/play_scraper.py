__author__ = 'grainier'

from pyquery import PyQuery as pq
import redis
import pickle

scraped_applications = []
user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:24.0) Gecko/20100101 Firefox/24.0'
set_key = 'set_priority_x'
r_server = redis.Redis("localhost")
application_keys = r_server.smembers(set_key)

for application_key in application_keys:
    serialized_application_raw_data = r_server.get(application_key)
    application_raw_data = pickle.loads(serialized_application_raw_data)

    application_id = application_raw_data['app_id']
    application_url = application_raw_data['app_url']

    application_soup = pq(
        application_url,
        headers={'User-Agent': user_agent}
    )

    body_content = application_soup('#body-content')

    ## application title
    app_title = body_content('.info-container .document-title').text()

    ## application thumbnail
    app_thumbnail = body_content('img.cover-image')[0].attrib['src']

    ## number of badges like Top Developer, Editors Choice
    special_badges = body_content('.header-star-badge .badge')
    number_of_badges = len(special_badges)

    ## application description
    description_content = body_content('.description .id-app-orig-desc')
    app_description = description_content.html()

    ## application rating value && count
    rating_box = body_content('.rating-box .score-container')
    rating_meta_data = rating_box('meta')
    rating_value = 0
    rating_count = 0
    for rating_meta in rating_meta_data:
        if rating_meta.attrib['itemprop'] == 'ratingValue':
            rating_value = rating_meta.attrib['content']
            pass
        elif rating_meta.attrib['itemprop'] == 'ratingCount':
            rating_count = rating_meta.attrib['content']
            pass
        pass

    ## make a application object
    application = {
        'title': app_title,
        'thumbnail': app_thumbnail,
        'badges': number_of_badges,
        'rating': rating_value,
        'rating_count': rating_count,
        'updated': 'updated',
        'installs': 'installs',
        'description': app_description
    }

    scraped_applications.append(application)
    pass

print('done')