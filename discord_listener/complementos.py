
import os
from googleapiclient.discovery import build
import random


api_key = "token google "



def buscarImagen(search):

    ran = random.randint(0, 9)
    resource = build("customsearch", "v1", developerKey=api_key).cse()
    result = resource.list(
        q=f"{search}", cx="token2", searchType="image"
    ).execute()
    url = result["items"][ran]["link"]


    return url




