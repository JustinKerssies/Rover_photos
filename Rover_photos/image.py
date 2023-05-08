"""
A new Photo class gets created every time there is a photo that needs to be depicted.
All the Photo classes end up in the 'id_list' in 'data.py'
"""

class Photo:

    def __init__(self, temp_dict):
        self.dict = temp_dict
        self.img_src = self.dict['img_src']

        self.questions = None
        self.responses = None

        self.width = None
        self.height = None
        self.ratio = None
