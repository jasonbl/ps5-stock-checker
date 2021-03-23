from enum import Enum

class PlaystationSeller(Enum):

    def __init__(self, seller_name, url):
        self.seller_name = seller_name
        self.url = url

    AMAZON = "Amazon", "https://www.amazon.com/PlayStation-5-Digital/dp/B08FC6MR62"
    GAME_STOP = "GameStop", "https://www.gamestop.com/video-games/playstation-5/consoles/products/playstation-5-digital-edition/11108141"
    BEST_BUY = "Best Buy", "https://www.bestbuy.com/site/sony-playstation-5-digital-edition-console/6430161.p?skuId=6430161"
    TARGET = "Target", "https://www.target.com/p/playstation-5-digital-edition-console/-/A-81114596"