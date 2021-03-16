from enum import Enum

class PlaystationSeller(Enum):

    def __init__(self, seller_name, url):
        self.seller_name = seller_name
        self.url = url

    AMAZON = "Amazon", "https://www.amazon.com/PlayStation-5-Digital/dp/B08FC6MR62"