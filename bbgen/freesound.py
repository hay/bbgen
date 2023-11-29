from random import choice
import os
import requests

ENDPOINT = "https://freesound.org/apiv2"

class Freesound:
    def __init__(self):
        self._key = os.environ["FREESOUND_API_KEY"]

    def _call(self, method: str, params: dict) -> dict:
        params.update({ "token" : self._key })
        req = requests.get(f"{ENDPOINT}/{method}", params = params)
        return req.json()

    def query(self, query, random = False):
        results = self._call("search/text", params = {
            "query" : query,
            "fields" : "name,id,previews"
        })

        # Either get the first result or a random one
        items = results["results"]

        if random:
            item = choice(items)
        else:
            item = items[0]

        # We can't download without doing oauth2 stuff
        # so just use preview
        # preview-hq-mp3