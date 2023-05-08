"""
    This file contains all the functions that receive the API responses
 """

import requests
from image import Photo
import shutil
from tkinter.ttk import Style, Progressbar

"""Response based functions"""

def api_response(s):
    # Receive the url\
    url = s.base_url
    url += s.search['name']
    url += s.url_addon
    # Retrieve all the added search specifications and add it to the url in a functional form
    for items in s.search:
        url += f'&{str(items)}={str(s.search[items])}'
    print(url)
    # Request the data from the API
    r = requests.get(url)
    response_dict = r.json()
    # If the length of the response dict == 0, it means there isn't any data within it
    if len(response_dict) == 0:
        return ''
    else:
        return response_dict


# noinspection PyTypeChecker
def retrieve_id(s):
    # retrieve API response (see above)
    temp_dict = api_response(s)

    # If it does not return temp_dict['photos'], there is no data within it,
    # so it returns true for the EMPTY variable in the app
    if not temp_dict['photos']:
        print(temp_dict)
        return True

    # It returned data, therefor for any item in temp_dict['photos'],
    # create a Photo class with all the individual data and add said class to the ID_list
    for item in temp_dict['photos']:
        photo = Photo(item)
        s.id_list.append(photo)
    return False


def show_image(photo):
    filename = 'temp_photo.png'
    # Request the img based on the img_src saved within the Photo class
    # (Also the timeout is there, because my home network doesn't want to deal with IPv6, on .gov.
    # Remove it for faster retrieval)
    try:
        r = requests.get(photo.img_src, stream=True, timeout=2)
    except TimeoutError:
        r = requests.get(photo.img_src, stream=True, timeout=20)

    # If the image has been successfully retrieved, download it as 'temp_photo.png'
    # and print that it has been successfully downloaded
    if r.status_code == 200:
        with open(filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
        return r.headers['Content-Type']
    else:
        print('Image Couldn\'t be retrieved')


def manifest_retrieval(s, name=None):
    if not name:
        rover = s.search['name']
    else:
        rover = name
    # if manifest already exists, return
    for items in s.manifest:
        if items == rover:
            return
    # create url
    url = s.manifest_url
    url += rover
    url += s.manifest_url_addon
    temp_lib = requests.get(url)
    response_dict = temp_lib.json()
    # save the manifest in data.py
    s.manifest[rover] = response_dict
    # for every date that is in the manifest, add it to possible dates in data.py,
    for i, date in enumerate(response_dict['photo_manifest']['photos']):
        date = response_dict['photo_manifest']['photos'][i]['earth_date']
        s.possible_dates[rover].append(date)
    # save the start and end date
    start_date = response_dict['photo_manifest']['photos'][0]['earth_date']
    end_date = response_dict['photo_manifest']['photos'][-1]['earth_date']
    s.start_and_end_date[rover] = [start_date, end_date]