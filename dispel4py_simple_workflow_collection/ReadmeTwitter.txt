 1. For storing the tweets ---> python get_live_tweets.py
	** Results are stored in tweets.json
 2. For executing the analysis ---->

	** You need to have several python packages installed for running this script
	   ** NLTK: http://www.nltk.org/install.html
	   ** pip install nltk numpy

	  vim twitter/analysis_sentiment.py ---> You could modify the ROOT_DIR if you want to indicate a different folder.
	  dispel4py simple twitter/analysis_sentiment.py  -d '{"read" : [ {"input" : "tweets.json"} ]}'



Steps to run get_live_tweets:
   To collect data you need a Twitter account and a Twitter application. Assuming you already have a Twitter account use the following instructions to create a Twitter application
	
   1. Create a Twitter application

    * Open a web browser and go to https://apps.twitter.com/app/new
    * Sign in with your normal Twitter username and password if you are not already signed in.
    * Enter a name, description, and temporary website (e.g. http://coming-soon.com)
    * Read and accept the terms and conditions – note principally that you agree not to distribute any of the raw tweet data and to delete tweets from your collection if they should be deleted from Twitter in the future.
    * Click "Create your Twitter application"
    * Click on the "API Keys" tab and then click "Create my access token"
    * Wait a minute or two and press your browser's refresh button (or ctrl+r / cmd+r)
    * You should now see new fields labeled "Access token" and "Access token secret" at the bottom of the page.
    * You now have a Twitter application that can act on behalf of your Twitter user to read data from Twitter.

  2. Connect your Twitter application to these scripts
    * Open get_live_tweets.py and enter your information here
	access_token_key = xxxxxxxx
	access_token_secret = xxxxxxx
	api_key = xxxxxxx
	api_secret = xxxxxx

