from dealz_api.mydealz_api import MydealzApi

api = MydealzApi()

processFreshDeals(api.get_fresh_deals())