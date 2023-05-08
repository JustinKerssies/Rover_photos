"""
This file has all the general functions that do not have much to do with Tkinter or API responses
It has general data sorting algorithms and calculations that would have bloated other files:
"""

from API import show_image
from PIL import Image


"""General functions"""


def adapt_current_photo_id(s, var):
    # If specified as 'next', add 1 to the current_ID, apart from if that would reach the end of the list
    if var == 'next':
        s.current_id += 1
        if s.current_id == len(s.id_list):
            s.current_id = 0
    # If specified as 'previous', subtract 1 from the current_id, apart from if that would make the ID be negative
    if var == 'previous':
        s.current_id -= 1
        if s.current_id < 0:
            s.current_id = len(s.id_list) - 1

    # Save the current Photo class based on the new 'current_id'
    current_photo = s.id_list[s.current_id]
    # Download the image based on the current Photo
    content_type = show_image(current_photo)
    current_photo.dict['content type'] = content_type
    # Return the current Photo class to 'app.py'
    return current_photo


def get_selected_name(data, selected_variable):
    if selected_variable == 2:
        data.search['name'] = 'Opportunity'
    elif selected_variable == 3:
        data.search['name'] = 'Spirit'
    else:
        data.search['name'] = 'Curiosity'


"""Data sort functions"""


def details_text_function(current_photo):
    # Request the current class Photo, and create temporary dictionaries, for both classifications and values
    photo = current_photo
    questions = []
    responses = []

    for items in photo.dict:
        # Remove 'img_src', as it is nothing more than just a link
        if not items == 'img_src':
            # Considering 'camera' and 'rover' are both their own lib, gotta make another 'for loop'
            if items == 'camera' or items == 'rover':
                for details in photo.dict[items]:
                    # Append everything into the class dicts (.questions and .responses)
                    questions.append(f'{items}.{str(details)}        :')
                    responses.append(f'{photo.dict[items][details]}')
            else:
                # Append everything else
                questions.append(f'{str(items)}        :')
                responses.append(f'{photo.dict[items]}')

    # Save the classifications and values within the Photo class
    photo.responses = responses
    photo.questions = questions


"""IMG based functions"""


def img_sizing(s, master, current_photo):
    # Open the 'temp_photo.png' and retrieve the current width and height
    img = Image.open("temp_photo.png")
    width = img.size[0]
    height = img.size[1]
    # Add the base width and height to the Photo.dict, to show them in the window
    width_height = f'{width} x {height}'
    current_photo.dict['base proportions'] = width_height
    # Calculate resize factors for both height and width
    master.update()
    master_width, master_height = master.winfo_width(), master.winfo_height()
    height_factor = master_height / height
    width_factor = master_width / width
    resize_factor = min(height_factor, width_factor)
    # Multiply width and height with the lowest of the factors, so both do not exceed the max given in 'data.py'
    width *= resize_factor
    height *= resize_factor
    # Add the current proportions and the resize factor to the window as well
    resize_factor = min(height_factor, width_factor)
    # Resize the pic based on what was calculated before
    return resize_factor


"""Manifest Button"""


def print_entire_manifest(s):
    rover = s.search['name']

    for items in s.manifest:
        if items == rover:
            for item in s.manifest[rover]['photo_manifest']:
                if not item == 'photos':
                    print(f'{item} : {s.manifest[rover]["photo_manifest"][item]}')
            for sol in s.manifest[rover]['photo_manifest']['photos']:
                print(sol)
            return
