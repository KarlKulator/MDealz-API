import datetime
import copy
import json

from dealz_api.action import Action
from dealz_api.fresh_deal import FreshDeal
from dealz_api.deal import Deal


def is_old_deal(deal, old_age_minutes):
    return deal.creation_date < datetime.datetime.now() - datetime.timedelta(
        minutes=old_age_minutes)


class HotDealAnalyzer:
    def __init__(self, configFile):
        with open(configFile, 'r') as file:
            config = json.load(file)
            self._ageToExclude_minutes = config['ageToExclude_minutes']
            self._ageToCheck_minutes = config['ageToCheck_minutes']
            self._numberOfCommentsThreshold = config['numberOfCommentsThreshold']

    def __call__(self, previous_deal: Deal, fresh_deal: FreshDeal, action_info: Action):
        previous_deal_new: Deal = copy.deepcopy(previous_deal)
        action_new: Action = copy.deepcopy(action_info)

        if previous_deal.hotnessChecked or fresh_deal.creation_date is None:
            return previous_deal_new, action_new

        if is_old_deal(deal=fresh_deal, old_age_minutes=self._ageToCheck_minutes) or fresh_deal.number_of_comments >= self._numberOfCommentsThreshold:
            previous_deal_new.hotnessChecked = True
            if fresh_deal.number_of_comments >= self._numberOfCommentsThreshold and not is_old_deal(fresh_deal, self._ageToExclude_minutes):
                action_new.hotness_triggered = True

        return previous_deal_new, action_new
