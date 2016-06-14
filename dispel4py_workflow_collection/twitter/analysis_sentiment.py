import sys
import json
import bisect
import nltk
from nltk.corpus import wordnet

from dispel4py.workflow_graph import WorkflowGraph
from dispel4py.core import GenericPE
from dispel4py.base import IterativePE, ConsumerPE

class ReadData(GenericPE): 
    def __init__(self):
        GenericPE.__init__(self)
        self._add_output('output')
	self.count = 0

    def process(self, inputs):
        twitterData= inputs['input']
        self.log("Reading tweets file %s" % ROOT_DIR + twitterData)
        tweet_file = open(ROOT_DIR + twitterData)
        for line in tweet_file:
            tweet = json.loads(line)
            text = coordinates = place = location = ''
            ## Get the tweet text
            text = tweet[u'text'].encode('utf-8')
            ## Get the tweet location
            if u'coordinates' in tweet and tweet[u'coordinates']:
                coordinates = tweet[u'coordinates'][u'coordinates']
            elif u'place' in tweet and tweet[u'place']:
                place = tweet[u'place'][u'full_name'].encode('utf-8')
            elif u'user' in tweet and tweet[u'user'][u'location']:
                location = tweet[u'user'][u'location'].encode('utf-8')
 	    self.count += 1	
            return_tweet={'text':text, 'coordinates':coordinates,'place':place, 'location':location}
            self.write('output',return_tweet)
	self.log("Total tweets found %s" % self.count)

class AFINNSentimeScore(IterativePE):
    def __init__(self, sentimentData):
        IterativePE.__init__(self)
        afinnfile = open(ROOT_DIR + sentimentData)
        self.sentiment= {}
        for line in afinnfile:
            term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
            self.sentiment[term] = float(score)  # Convert the score to an integer.
	self.method = 'AFINN' 	
    def _process(self, data):
        tweet =  data
	avg_score = 0
	count = 0
        tweet_word = nltk.word_tokenize(tweet['text'])
        sent_score = 0 # sentiment score della frase
        for word in tweet_word:
             word = word.rstrip('?:!.,;"!@')
             word = word.replace("\n", "")
             if not (word.encode('utf-8', 'ignore') == ""):
                 if word.encode('utf-8') in self.sentiment.keys():
                     sent_score = sent_score + float(self.sentiment[word])
		     count += 1
	if count <> 0:	
            avg_score = sent_score/count
	else:
	    avg_score = sent_score	 	
	return(tweet, avg_score, self.method)


class PrintAFINNScore(ConsumerPE):
    def __init__(self):
        ConsumerPE.__init__(self)
    def _process(self, data):
	tweet, sent_score = data
        self.log("Tweet %s --- score %s " % ( tweet['text'], str(sent_score)))
	filename=ROOT_DIR+ "Afiinscored.txt"
	with open(filename, "a+") as results:
		results.write(tweet['text'] + " ------score: "+  str(sent_score) + "\n")
	

class FindState(IterativePE):
    def __init__(self):
        IterativePE.__init__(self)
        self.US_states={}  
        self.US_states=self.load_states("us-states.json")
    def _process(self, data):
        tweet,sent_score, method = data
        state = self.find_state(tweet)
        if state:
            self.write('output', [tweet, sent_score, state, method])
    def find_state(self, tweet):
        ## First look at the coordinates attribute
        if tweet['coordinates']:
           coord = tweet['coordinates']
           return self.coord2state(coord)
        ## Then look at the place attribute
        elif tweet[u'place']:
            place = tweet['place']
            place = " "+place+" "
            state_abbr = [s for s in self.US_states['abbr'] if " "+s+" " in place.upper()]
            if state_abbr:
                return state_abbr[0]
        ## Finally look at the user location attribute
        elif tweet[u'location']:
            location = tweet['location']
            location = " " + location + " "
            state_abbr = [s for s in self.US_states['abbr'] if " "+s+" " in location.upper()]
            state_name = [s for s in self.US_states['name'] if s.lower() in location.lower()]
            if state_abbr:
                return state_abbr[0]
            elif state_name:
                state_idx = self.US_states['name'].index(state_name[0])
                return self.US_states['abbr'][state_idx]
        return ''

    def load_states(self, us_file):
        US_states = {'name': [], 'abbr': [], 'coord': []}
        filename= ROOT_DIR + us_file
        states_file = open(filename, "r")
        features = json.load(states_file)[u'features']
        for f in features:
            US_states['name'].append(f[u'properties'][u'name'].encode('utf-8'))
            US_states['abbr'].append(f[u'properties'][u'state'].encode('utf-8'))
            coord = f[u'geometry'][u'coordinates'][0]
            if len(coord)==1: coord = coord[0]
            US_states['coord'].append(coord)
	return US_states	

    def coord2state(self,coord):
        ## Check if the given location is within the state boundaries
        picked = []
        for i in range(len(self.US_states['name'])):
            ## Calculate the boundary box of the state
            xy = self.US_states['coord'][i]
            xmin = min(xy, key=lambda x:x[0])
            xmax = max(xy, key=lambda x:x[0])
            ymin = min(xy, key=lambda x:x[1])
            ymax = max(xy, key=lambda x:x[1])
            ## Check if the location is inside the box
            if (coord[0] >= xmin) and (coord[0] <= xmax) and (coord[1] >= ymin) and (coord[1] <= ymax):
                picked.append(i)

        if len(picked) == 0:
             return ''

        if len(picked) == 1:
            return self.US_states['abbr'][picked[0]]

        ## If multiple states are found, pick the one that has
        ## the shortest distance from its center to the location
        d = []
        for k in picked:
            xcenter = 0.5 * sum(x for x,y in self.US_states['coord'][k])
            ycenter = 0.5 * sum(y for x,y in self.US_states['coord'][k])
            d.append( (x-xcenter)**2+(y-ycenter)**2 )
        idx = d.index(min(d))
        return self.US_states['abbr'][idx]


class HappyState(GenericPE):
    def __init__(self):
        GenericPE.__init__(self)
        self._add_input ('input', grouping=[2,3])
        self._add_output('output')
        self.mood = {}
        self.happiest = -5000, None
    def _process(self, inputs):
        tweet, sent_score, state, method = inputs['input']
        
        if state not in self.mood:
            self.mood[state] = sent_score
        else:
            self.mood[state] +=sent_score
        
        happiest_state, happiest_score= self.happiest
        
        if self.mood[state] > happiest_score:
            happiest_score = self.mood[state]
            self.happiest = state, happiest_score 
            #self.log("!!!Happiest country is %s, score = %s"  % (state, happiest_score))
            self.write('output', [state, happiest_score,method ])

class GlobalHappyState(GenericPE):
    def __init__(self):
        GenericPE.__init__(self)
        self._add_input ('input', grouping='global')
        self.state = None
        self.happiness={} #pair state, sentiment
        self.top_number = 3  
        self.top_states = []
        self.top_scores = []
	self.total_tweets = 0
    def _process(self, inputs):
        state, score, method = inputs['input']
	self.total_tweets += 1
        #self.log('new max for %s: (%s, %s)' % (method, state, score))
        self.happiness[state]=score 
        try:
            state_index = self.top_states.index(state)
            del self.top_states[state_index]
            del self.top_scores[state_index]
        except ValueError:
            pass
        index = bisect.bisect_left(self.top_scores, score)
        self.top_scores.insert(index, score)
        self.top_states.insert(index, state)
        if len(self.top_scores) > self.top_number:
            self.top_scores.pop(0)
            self.top_states.pop(0)
        self.score = self.top_scores[0]
	count = 0
        for (score, state) in zip(self.top_scores, self.top_states):
            self.log("METHOD:%s - top:%s----> state = %s, score = %s, total_tweets = %s"  % (method, count, state, score, self.total_tweets))
            count += 1


ROOT_DIR="twitter/"	
tweets= ReadData() 
tweets.name='read'
sentiment_afinn= AFINNSentimeScore("AFINN-111.txt")            
findstate1=FindState()
happystate1=HappyState()
findhappystate1 = GlobalHappyState()


graph = WorkflowGraph()
graph.connect(tweets, 'output', sentiment_afinn, 'input')
graph.connect(sentiment_afinn, 'output', findstate1, 'input')
graph.connect(findstate1, 'output', happystate1, 'input')
graph.connect(happystate1, 'output', findhappystate1, 'input')

