# SI507 Final Project

## How to run my code:

If you only want to see the demo, you can just run Step3_Demo.py under Python environment. Then, you can go to http://localhost:5000/ to see the interactive interface. All the supported functions are listed on the left. After you click these options, you will be provided detailed instructions on how to interact. You can type into words and click "submit" to see its reaction.

If you want to run the whole process, you should run all code blocks in Step1_Data_Caching.ipynb and Step2_Data_Structuring.ipynb. Since the caching of websites are too large, I didn't upload them into github. So you need approximately 10 minutes to run Step1 for the first time (if you cached it before, it will automatically skip the process). Step2 is used for processing the crawled data, turn them into graph structure and store into json file, and it will take about 3 seconds to finish all the job.

Required packages:

Step 1: requests, pandas, bs4.BeautifulSoup
Step 2: pandas
Step 3: flask, plotly


## Step 1: Data Caching

The detailed caching process is shown in Project Report.

The code file is Step1_Data_Caching.ipynb

## Step 2: Data Structuring

I used dict structure to construct my graph. Whether or not two restaurants are linked depends on the number of "tags" they share. For famous restaurants, there're many tags created by users (which is crawled in "Strong_tag" field of my data). However, 1/3 of restaurants don't have these user-created tags. To solve this problem, I also crawled all the restaurant review text in my dataset, and use the "Strong tags" list to match the tags in the reviews. By using this method, I created plenty of tags for every restaurant in my dataset.

Then, for restaurants that share the same tags, they can be considered as "linked". The more tags they share, the stronger they link together. We can build a graph based on this relationship. If restaurant 0 and 1 share the same tags [pizza, burger, chips], then our graph dictionary structure can be {0: {1: [pizza, burger, chips]}} and {1: {0: [pizza, burger, chips]}}. By this method, we built a large graph, which is stored in graph_dict.json.

The python file I used to construct this graph is Step2_Data_Structuring.ipynb. I put many notes in the notebook for better understanding the steps.

## Step 3: Data Presenting

Shown in the report!

The code is in Step3_Demo.py, and demo_support.py provides several support functions used in Step3_Demo.py.