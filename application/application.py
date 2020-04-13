import time

from dealz_api.action_executor import ActionExecutor
from dealz_api.keyword_alarm_analyzer import KeywordAlarmAnalyzer
from dealz_api.mydealz_api import MydealzApi
from dealz_api.fresh_deals_processor import FreshDealsProcessor
from dealz_api.deals_database import DealsDatabase

api = MydealzApi()
processor = FreshDealsProcessor(DealsDatabase())
analyzer = KeywordAlarmAnalyzer('../dealz_api/config/keyword_alarm_analyzer.json')
executor = ActionExecutor('../dealz_api/config/action_executor.json')
processor.add_deal_analyzer(analyzer)
processor.set_action_executor(executor)

while(True):
    fresh_deals = api.get_fresh_deals()
    processor.process_fresh_deals(fresh_deals)
    time.sleep(10)
