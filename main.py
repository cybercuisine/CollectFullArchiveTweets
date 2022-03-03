import pandas as pd
import requests
import time
import gc
import os
import json

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = os.environ.get("BEARER_TOKEN")
search_url = "https://api.twitter.com/2/tweets/search/all"

data_path = "<path of directory you want to save data>"

# Optional params: start_time,end_time,since_id,until_id,max_results,next_token,
# expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields
query_params = {'query': '<write your search query>',
                'start_time': 'yyyy-mm-ddThh:mm:ssZ',
                'end_time': 'yyyy-mm-ddThh:mm:ssZ',
                'max_results': 100,
                'expansions': 'author_id',
                'tweet.fields': 'id,text,created_at,public_metrics',
                'user.fields': 'description,id,name',
                'place.fields': 'country,country_code'}
columns = ["author_id", "tweet_id", "text", "created_at", "faves", "retweets", "replies", "quotes",
           "user_description", "user_id", "name", "username"]


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2FullArchiveSearchPython"
    return r


class SearchTweets:
    def __init__(self, datapath):
        self.datapath = datapath

    @staticmethod
    def connect_to_endpoint(url, params):
        response = requests.request("GET", url, auth=bearer_oauth, params=params, timeout=(5.0, 7.0))
        if response.status_code != 200:
            raise Exception(response.status_code, response.text)
        return response.json()

    @staticmethod
    def json2df(json_response):
        df1 = pd.DataFrame(columns=columns)

        for s, t in zip(json_response["data"], json_response["includes"]["users"]):
            author_id = s["author_id"]
            tweet_id = s["id"]
            text = s["text"]
            created_at = s["created_at"]
            faves = s["public_metrics"]["like_count"]
            retweets = s["public_metrics"]["retweet_count"]
            replies = s["public_metrics"]["reply_count"]
            quotes = s["public_metrics"]["quote_count"]
            user_description = t["description"]
            user_id = t["id"]
            name = t["name"]
            username = t["username"]

            res = [author_id, tweet_id, text, created_at, faves, retweets,
                   replies, quotes, user_description, user_id, name, username]

            df1.loc[df1.shape[0], :] = res

        return df1


    def write_next_token(self, NextToken):
        with open(f"{self.datapath}/next_log.txt", mode='a', encoding='utf-8') as f:
            f.write(NextToken)
            f.write('\n')
        with open(f"{self.datapath}/next.txt", mode='w', encoding='utf-8') as f:
            f.write(NextToken)


    def MakeData(self, filenum):
        data = f'{self.datapath}/data{filenum}.pkl'
        print(data)
        dataframe = pd.DataFrame(columns=columns)
        while True:
            try:
                time.sleep(1)
                json_response = self.connect_to_endpoint(search_url, query_params)
            except Exception as e:
                dataframe.to_pickle(data)
                time.sleep(15 * 60)
                json_response = self.connect_to_endpoint(search_url, query_params)

            dataframe = pd.concat([dataframe, self.json2df(json_response)])
            if 'next_token' in json_response['meta']:
                next_token = json_response['meta']['next_token']
                self.write_next_token(next_token)
                query_params['next_token'] = next_token
            else:
                dataframe.to_pickle(data)
                return False

            if dataframe.shape[0] >= 50000:
                dataframe.to_pickle(data)
                return True


def main(path):
    filenum = 1
    st = SearchTweets(path)
    while st.MakeData(filenum):
        filenum += 1
        gc.collect()
    print("program finished")


if '__name__' == '__main__':
    main(data_path)
