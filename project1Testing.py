import pandas as pd
import json
from collections import Counter
from nltk import ngrams
from nltk.collocations import *
import re
import numpy as np
from json_to_pd import *
import pdb

OFFICIAL_AWARDS = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']

def award_dictionary():
    
    stop_words = ['i',
                  'me',
                  'my',
                  'myself',
                  'we',
                  'our',
                  'ours',
                  'ourselves',
                  'you',
                  'your',
                  'yours',
                  'yourself',
                  'yourselves',
                  'he',
                  'him',
                  'his',
                  'himself',
                  'she',
                  'her',
                  'hers',
                  'herself',
                  'it',
                  'its',
                  'itself',
                  'they',
                  'them',
                  'their',
                  'theirs',
                  'themselves',
                  'what',
                  'which',
                  'who',
                  'whom',
                  'this',
                  'that',
                  'these',
                  'those',
                  'am',
                  'is',
                  'are',
                  'was',
                  'were',
                  'be',
                  'been',
                  'being',
                  'have',
                  'has',
                  'had',
                  'having',
                  'do',
                  'does',
                  'did',
                  'doing',
                  'a',
                  'an',
                  'the',
                  'and',
                  'but',
                  'if',
                  'or',
                  'because',
                  'as',
                  'until',
                  'while',
                  'of',
                  'at',
                  'by',
                  'for',
                  'with',
                  'about',
                  'against',
                  'between',
                  'into',
                  'through',
                  'during',
                  'before',
                  'after',
                  'above',
                  'below',
                  'to',
                  'from',
                  'up',
                  'down',
                  'in',
                  'out',
                  'on',
                  'off',
                  'over',
                  'under',
                  'again',
                  'further',
                  'then',
                  'once',
                  'here',
                  'there',
                  'when',
                  'where',
                  'why',
                  'how',
                  'all',
                  'any',
                  'both',
                  'each',
                  'few',
                  'more',
                  'most',
                  'other',
                  'some',
                  'such',
                  'no',
                  'nor',
                  'not',
                  'only',
                  'own',
                  'same',
                  'so',
                  'than',
                  'too',
                  'very',
                  's',
                  't',
                  'can',
                  'will',
                  'just',
                  'don',
                  'should',
                  'now',
                  '-']

    empty_dict = {}
    for award in OFFICIAL_AWARDS:
        filtered_sentence = [w for w in award.split(' ') if not w in stop_words]
        empty_dict[award] = filtered_sentence
    return empty_dict



def pre_ceremony():
    '''This function loads/fetches/processes any data your program
        will use, and stores that data in your DB or in a json, csv, or
        plain text file. It is the first thing the TA will run when grading.
        Do NOT change the name of this function or what it returns.'''
    global data
    # Your code here
    with open('gg2013.json') as f:
        data = json.load(f)

    Id = []
    text = []
    timestamp = []
    user_id = []
    screen_name = []

    for row in data:
        Id.append(row['id'])
        text.append(row['text'])
        timestamp.append(row['timestamp_ms'])
        user_id.append(row['user']['id'])
        screen_name.append(row['user']['screen_name'])
    
    global table2013
    table2013 = pd.DataFrame({'text':text,'timestamp':timestamp,'user_id':user_id,'user_screen_name':screen_name},index=Id)
    table2013.index.rename('id',inplace=True)


    global award_dict
    award_dict = award_dictionary()


    return


def get_winner(year):
    '''Winners is a dictionary with the hard coded award
    names as keys, and each entry containing a single string.
    Do NOT change the name of this function or what it returns.'''
    # Your code here
    if year == '2013':
        table = table2013
    for award in award_dict:
        candidate_tweets = award_tweets(table,award,['win'])
        if 'performance' in award_dict[award]:
            winner_tweets = " ".join(candidate_tweets) #merge to one string
            winner_tweets = re.sub(r'\b%s\b' % 'Golden Globes|Motion|Picture|Performance|Best', '', winner_tweets) #Remove the term Golden Globes
            ngram_counts = Counter(ngrams(winner_tweets.split(), 2)) #Create list of bigrams
            top_bigrams = ngram_counts.most_common(10) #Find top 10
            names = [bigram[0][0]+' '+bigram[0][1] for bigram in top_bigrams if bigram[0][0][0].isupper() and bigram[0][1][0].isupper()] #Filter out bigrams that aren't both capitalized
            print(award)
            print(names)


    #return winners




def get_nominees(year):
	table = table2013
	for award in award_dict:
		nom_tweets = award_tweets(table,award,['nominee', 'nominees', 'nominating', 'nominated', 'nominates', 'Nominee', 'Nominees', 'Nominating', 'Nominated', 'Nominates'])
		print (award)
		for tweet in nom_tweets:
			print (tweet)
			print('\n')
		print("\n\n\n\n\n\n\n\n")

	#for award in actor_award_dict:
	#return nominees 

def get_nominees_test(year):
	with open('gg2013answers.json', 'r') as f:
	    answers = json.load(f)
	nom_dict = {}
	table = table2013
	for award in award_dict:
		#nom_tweets = award_tweets(table,award, ['nomin', 'Nomin', 'deserved to win', "should've won", 'should have won', 'deserved', 'hope', 'better win', "didn't win"])
		nom_tweets = award_tweets(table,award,[''])
		#print(nom_tweets)
		#print(len(nom_tweets))
		allTweets = " ".join(nom_tweets) #merge to one string
		allTweets = allTweets.lower()
		print(award)
		print('total number of tweets after filtering using award_tweets:')
		print(len(nom_tweets))
		print('\n')
		print('winner:')
		winner = answers['award_data'][award]['winner']
		print(winner + '\n')
		print(countOccurences(allTweets,winner))
		print('\n')
		print('nominees:')
		for noms in answers['award_data'][award]['nominees']:
			count = countOccurences(allTweets,noms)
			print(noms + '\n')
			print(count)
			print('\n')

		# for tweet in nom_tweets:
		# 	print (tweet)
		# 	print('\n')

	print('\n\n\n\n\n\n')


def countOccurences(longString, subString):
	count = 0
	start = 0
	flag = True
	while flag:
		a = longString.find(subString,start)
		if a == -1:
			flag=False
		else:
			count += 1
			start = a + 1
	return count

	#nom_tweets = award_tweets(table, award, [''])
	# for tweet in nom_tweets:
	# 	print(tweet)
	# 	print('\n')

	# for award in award_dict:
	# 	print(award)


def award_tweets(table,award,keywords):
    relevant_tweets = [tweet for tweet in table['text'] if keyword_present(tweet,keywords)]
    high_score = max([(sum([1 for word in award_dict[award] if word in tweet.lower()])) for tweet in relevant_tweets])
    win_candidates = [tweet for tweet in relevant_tweets if sum([1 for word in award_dict[award] if word in tweet.lower()]) in [high_score,(high_score-1),(high_score-2)]]
    return win_candidates

def keyword_present(tweet,keywords):
    for keyword in keywords:
        if keyword in tweet:
            return True
    return False


pre_ceremony()
#print(data[400:600])
#print(award_dictionary()['best motion picture - drama'])
#print(get_winner('2013'))

#get_nominees('2013')

get_nominees_test('2013')



