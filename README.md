# CollectFullArchiveTweets
You can collect tweets full archive via TwitterAPI2 by customizing this program.

# Requirements
- You should be approved Twitter Academic Research to use this program.
  - Twitter Academic Research: https://developer.twitter.com/en/products/twitter-api/academic-research
  - However, with proper customizing, you can use this program by APIs other than academic research API.
- You need python environments. Read the file "requirements.txt" to know details.
- data will be stored as pickle files.

# Usage
First, clone this repository.
## Set BEARER_TOKEN
In terminal, run the following line:<br>
```
export 'BEARER_TOKEN'='<your_bearer_token>'
```
## Customize program
In main.py, the global variables "data_path" and "query_params" will be found. Customize these variables. 
- "data_path" defines directory collected data will be stored.
- "query_params" details: https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query
  - If you want to add elements to "query_params", you need to customize the variable "columns" and the function "json2df"
- If you use API other than academic research, change the variables "search_url" for your API.

## Run the program
After setting bearer_token and customizing, run the following line:
```
python main.py
```
The program will take huge time, so while waiting for program finished, drink a cup of coffee and prepare today's dinner .


# Citations
https://github.com/twitterdev/Twitter-API-v2-sample-code/blob/main/Full-Archive-Search/full-archive-search.py
