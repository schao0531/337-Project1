'''Version 0.2'''
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

def keyword_present(tweet,keywords):
    for keyword in keywords:
        if keyword in tweet:
            return True
    return False

def award_tweets(table,award,keywords):
    '''f'''
    
    relevant_tweets = [tweet for tweet in table['text'] if keyword_present(tweet,keywords)]
    high_score = max([(sum([1 for word in award_dict[award] if word in tweet.lower()])) for tweet in win_tweets])
    win_candidates = [tweet for tweet in win_tweets if sum([1 for word in award_dict[award] if word in tweet.lower()]) == high_score]
    return win_candidates

def get_hosts(year):
    '''Hosts is a list of one or more strings. Do NOT change the name
    of this function or what it returns.'''

    if year == '2013':
      table = table2013

#    elif year == '2015':
#      table = table2015

    filtered_tweets = table.loc[(table['text'].str.contains('host|Host', regex=True)) & ~(table['text'].str.contains('next|Next', regex=True)) ]['text'] #contains word host, does not contain next
    host_tweets = " ".join(filtered_tweets) #merge to one string
    host_tweets = re.sub(r'\b%s\b' % 'Golden Globes', '', host_tweets) #Remove the term Golden Globes
    ngram_counts = Counter(ngrams(host_tweets.split(), 2)) #Create list of bigrams
    top_bigrams = ngram_counts.most_common(10) #Find top 10
    names = [bigram[0][0]+' '+bigram[0][1] for bigram in top_bigrams if bigram[0][0][0].isupper() and bigram[0][1][0].isupper()] #Filter out bigrams that aren't both capitalized
    return names

def get_awards(year):
    '''Awards is a list of strings. Do NOT change the name
    of this function or what it returns.'''

        #generalize to any award shows
    award_words = ['Motion', 'motion', 'Picture', 'picture', 'Drama', 'drama', 'Performance', 'performance', 'Actress', 'actress', 'Actor', 'actor','Comedy', 'comedy', 'Musical', 'musical', 'Animated', 'animated', 'Feature', 'feature', 'Film', 'film', 'Foreign', 'foreign', 'Language', 'language', 'Supporting', 'supporting', 'Role', 'role', 'Director', 'director', 'Screenplay', 'screenplay', 'Original', 'orginal', 'Score', 'score', 'Song', 'song', 'Television', 'television', 'Series', 'series', 'Mini-series',  'mini-series', 'mini', 'Mini']
    helper_regex = r"(Best(?=\s[A-Z])(?:\s([A-Z]\w+|in|a|by an|for|or|\s-\s))+)"
    stop_words = ['the', 'The', 'a', 'A', 'for', 'For', 'in', 'In', 'by', 'By','an', 'An']

    #for rest of awards, dictionary from official award name to common name

    #awards_list = set()
    awards_list = []

    if year == '2013':
        table = table2013

    filtered_awards = table.loc[(table['text'].str.contains(helper_regex, regex=True))]['text']

    for t_id, text in filtered_awards.iteritems():
      match = re.search(helper_regex, text)
      if match:
        #print(match)
        award_name = match.group(0)
        award_name = re.sub(r'\b%s\b' % 'Golden Globes', '', award_name) #Remove the term Golden Globes
        award_name = re.sub(r'(television\s+series)|(tv\s+series)', 'TV Series', award_name, flags=re.IGNORECASE)
        words = award_name.split()
        if (len(words) > 1) and (any(x in words for x in award_words)):
          awards_list.append(award_name)

    #awards_list = list(awards_list)
    #print(Counter(awards_list))
    most_common_awards = Counter(awards_list).most_common(15)
    #awards = "\n".join(awards_list)

    awards = [x[0] for x in most_common_awards]
    print(awards)
    return awards

def get_nominees(year):
    '''Nominees is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change
    the name of this function or what it returns.'''
    # Your code here
    return nominees

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
    
    return winners

def get_presenters(year):
    '''Presenters is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change the
    name of this function or what it returns.'''
    # Your code here
    return presenters

def pre_ceremony():
    '''This function loads/fetches/processes any data your program
        will use, and stores that data in your DB or in a json, csv, or
        plain text file. It is the first thing the TA will run when grading.
        Do NOT change the name of this function or what it returns.'''
    
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

    """
    with open('gg2015.json') as f:
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
    
    global table2015
    table2015 = pd.DataFrame({'text':text,'timestamp':timestamp,'user_id':user_id,'user_screen_name':screen_name},index=Id)
    table2015.index.rename('id',inplace=True)
    """

    return

def main():
    '''This function calls your program. Typing "python gg_api.py"
    will run this function. Or, in the interpreter, import gg_api
    and then run gg_api.main(). This is the second thing the TA will
    run when grading. Do NOT change the name of this function or
    what it returns.'''

    pre_ceremony()
    get_awards("2013")
    return

if __name__ == '__main__':
    main()
