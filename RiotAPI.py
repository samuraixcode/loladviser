import RiotConsts as Consts
import requests

class RiotAPI(object):
    def __init__(self, api_key, region=Consts.REGIONS['europe_nordic_and_east']):
        self.api_key = api_key
        self.region = region

    def _request(self, api_url, params={}):
        args = {'api_key': self.api_key}
        for key, value in params.items():
            if key not in args:
                args[key] = value
        response = requests.get(
                Consts.URL['base'].format(
                        proxy=self.region,
                        region=self.region,
                        url=api_url),
                params=args)
        return response.json()

    def get_summoner_by_name(self, name):
        api_url = Consts.URL['summoner_by_name'].format(
                version=Consts.API_VERSIONS['summoner'],
                name=name)
        return self._request(api_url)

    def get_summoner_by_id(self, id):
        api_url = Consts.URL['summoner_by_id'].format(
                version=Consts.API_VERSIONS['matchlist'],
                summonerId=id)
        return self._request(api_url)
    
    def get_match_by_id(self, id):
        api_url = Consts.URL['match_by_id'].format(
                version=Consts.API_VERSIONS['match'],
                matchId=id)
        return self._request(api_url)
    