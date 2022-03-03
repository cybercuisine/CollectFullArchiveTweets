# CollectFullArchiveTweets
You can collect tweets full archive via TwitterAPI2 by customizing this program.

# Requirements
- You should be approved Twitter Academic Research to use this program.
  - Twitter Academic Research: https://developer.twitter.com/en/products/twitter-api/academic-research
  - However, with proper customizing, you use this program by APIs other than academic research API.
- You need python environments. Read the file "requirements.txt" to know details.
- data will be stored as pickle files.

# Usage
## Set BEARER_TOKEN
Run following code in terminal:<br>
```
export 'BEARER_TOKEN'='<your_bearer_token>
```
## Customize program
In main.py, the global variables "datapath" and "query_params" will be found. Customize these variables. 
- "datapath" defines directory collected data will be stored.
- "query_params" details: https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-quer
  - If you want to add elements to "query_params", you need to customize the variable "columns" and the function "json2df"

# Citations
https://github.com/twitterdev/Twitter-API-v2-sample-code/blob/main/Full-Archive-Search/full-archive-search.py
