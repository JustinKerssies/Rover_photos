"""
    File with all the settings, variables and static data that the other files use
"""


class Settings:

    def __init__(self):
        """Initialized data"""
        self.search = {
            'api_key': 'YmvafDmRogIwtQg4HDtb8L9y5lWdICmAl1hkPIgy'
        }
        self.id_list = []
        self.current_id = 0
        self.favorite_sorting_list = {}
        self.progressbar_loc = None
        self.progressbar_text = None

        """IMG data"""
        self.max_pic_height = 580
        self.max_pic_width = 1100
        self.max_zoom = 5
        self.zoom_delta = 0.8

        """Search data"""
        # API Static Data
        self.base_url = 'https://api.nasa.gov/mars-photos/api/v1/rovers/'
        self.url_addon = '/photos?'
        self.manifest_url = 'https://api.nasa.gov/mars-photos/api/v1/manifests/'
        self.manifest_url_addon = '?api_key=YmvafDmRogIwtQg4HDtb8L9y5lWdICmAl1hkPIgy'
        self.rovers = ['Curiosity', 'Opportunity', 'Spirit']

        """Camera Data"""
        self.camera_options_all = [
            'ENTRY',
            'EMPTY',
            'Mast Camera (MAST)',
            'Chemistry and Camera Complex (CHEMCAM)',
            'Mars Hand Lens Imager (MAHLI)',
            'Mars Decent Imager (MARDI)',
            'Front Hazard Avoidance Camera (FHAZ)',
            'Rear Hazard Avoidance Camera (RHAZ)',
            'Navigation Camera (NAVCAM)',
            'Panoramic  Camera (PANCAM)',
            'Miniature Thermal Emission Spectrometer (MINITES)'
        ]
        self.camera_options = [
            'Empty'
        ]
        """Favorite Data"""
        self.fav_list = []
        self.favorite = False

        self.favorite_sorting_list = {}

        """Date data"""
        self.possible_dates = {
            'Curiosity': [],
            'Opportunity': [],
            'Spirit': []
        }
        self.start_and_end_date = {
            'Curiosity': [],
            'Opportunity': [],
            'Spirit': []
        }
        self.currently_selected_date = []

        """Other Data"""
        self.manifest = {}
        self.sol_tooltip = 'Curiosity:  Sol = 0 - 3788' \
                           '\nOpportunity:  Sol = 1 - 5111' \
                           '\nSpirit:  Sol = 1 - 2208' \
                           '\nKeep in mind some sols might not work, as no pictures were taken on that sol'
        self.earth_date_tooltip = 'Curiosity:  Date = 2012-08-06 - 2023-04-03' \
                                  '\nOpportunity:  Date = 2004-01-26 - 2018-06-11' \
                                  '\nSpirit:  Date = 2004-01-05 - 2010-03-21' \
                                  '\nKeep in mind some dates might not work, as no pictures were taken on that date'

    def initialize(self):
        """Reset Data"""
        print('INITIALIZING!')
        self.search = {
            'api_key': 'YmvafDmRogIwtQg4HDtb8L9y5lWdICmAl1hkPIgy'
        }
        self.id_list = []
        self.current_id = 0
        self.favorite_sorting_list = {}
        self.currently_selected_date = []
