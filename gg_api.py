import pandas as pd
import json
import nltk
nltk.download('punkt', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)
nltk.download('maxent_ne_chunker', quiet=True)
nltk.download('words', quiet=True)
from collections import Counter
from nltk import ngrams
from nltk.collocations import *
import re
import pdb
import sys
import warnings
warnings.filterwarnings("ignore", 'This pattern has match groups')

OFFICIAL_AWARDS_1315 = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']
OFFICIAL_AWARDS_1819 = ['best motion picture - drama', 'best motion picture - musical or comedy', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best performance by an actress in a motion picture - musical or comedy', 'best performance by an actor in a motion picture - musical or comedy', 'best performance by an actress in a supporting role in any motion picture', 'best performance by an actor in a supporting role in any motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best motion picture - animated', 'best motion picture - foreign language', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best television series - musical or comedy', 'best television limited series or motion picture made for television', 'best performance by an actress in a limited series or a motion picture made for television', 'best performance by an actor in a limited series or a motion picture made for television', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best performance by an actress in a television series - musical or comedy', 'best performance by an actor in a television series - musical or comedy', 'best performance by an actress in a supporting role in a series, limited series or motion picture made for television', 'best performance by an actor in a supporting role in a series, limited series or motion picture made for television', 'cecil b. demille award']

table = None
award_dict = None

def award_dictionary(year):
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
    OFFICIAL_AWARDS = []
    if year == "2013":
        OFFICIAL_AWARDS = OFFICIAL_AWARDS_1315
    elif year == "2018":
        OFFICIAL_AWARDS = OFFICIAL_AWARDS_1819
    for award in OFFICIAL_AWARDS:
        if "television" in award:
            award_name = re.sub(r'(television\s+series)|(tv\s+series)', 'TV Series', award, flags=re.IGNORECASE)
        filtered_sentence = [w for w in award.split(' ') if not w in stop_words]
        empty_dict[award] = filtered_sentence
    return empty_dict

def keyword_present(tweet,keywords):
    for keyword in keywords:
        if keyword.lower() in tweet.lower():
            return True
    return False

def award_tweets(table,award,keywords):
    global award_dict
    relevant_tweets = [tweet for tweet in table['text'] if keyword_present(tweet,keywords)]
    high_score = max([(sum([1 for word in award_dict[award] if word in tweet.lower()])) for tweet in relevant_tweets])
    win_candidates = [tweet for tweet in relevant_tweets if sum([1 for word in award_dict[award] if word in tweet.lower()]) == high_score]
    return win_candidates

def fill_res_dict(year):
    hosts = get_hosts(year)
    awards = get_awards(year)
    #nominees = get_nominees(year)
    #winners = get_winners(year)
    presenters = get_presenters(year)

    res_dict = {}
    res_dict["hosts"] = hosts

    res_dict["award_data"] = {}
    for a in awards:
        res_dict["award_data"][a] = {}

    i = 0

    OFFICIAL_AWARDS = []
    if year == "2013":
        OFFICIAL_AWARDS = OFFICIAL_AWARDS_1315
    elif year == "2018":
        OFFICIAL_AWARDS = OFFICIAL_AWARDS_1819

    for award in awards:
        pdb.set_trace()
        res_dict["award_data"][award] = {}
        #res_dict["award_data"][award]["presenters"] =

def get_hosts(year):


    '''Hosts is a list of one or more strings. Do NOT change the name
    of this function or what it returns.'''

    global table
    if table is None:
        pre_ceremony(year)

    print("\nGetting the ceremony hosts...")
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
    global table
    if table is None:
        pre_ceremony(year)

    print("\nGetting the award categories...")
    award_words = ['Motion', 'motion', 'Picture', 'picture', 'Drama', 'drama', 'Performance', 'performance', 'Actress', 'actress', 'Actor', 'actor','Comedy', 'comedy', 'Musical', 'musical', 'Animated', 'animated', 'Feature', 'feature', 'Film', 'film', 'Foreign', 'foreign', 'Language', 'language', 'Supporting', 'supporting', 'Role', 'role', 'Director', 'director', 'Screenplay', 'screenplay', 'Original', 'orginal', 'Score', 'score', 'Song', 'song', 'Television', 'television', 'Series', 'series', 'Mini-series',  'mini-series', 'mini', 'Mini']
    helper_regex = r"(Best(?=\s[A-Z])(?:\s([A-Z]\w+|in|a|by an|for|or|\s-\s))+)"

    awards_list = []

    filtered_awards = table.loc[(table['text'].str.contains(helper_regex, regex=True))]['text']

    for t_id, text in filtered_awards.iteritems():
      match = re.search(helper_regex, text)
      if match:
        award_name = match.group(0)
        award_name = re.sub(r'\b%s\b' % 'Golden Globes', '', award_name) #Remove the term Golden Globes
        award_name = re.sub(r'(television\s+series)|(tv\s+series)', 'TV Series', award_name, flags=re.IGNORECASE)
        words = award_name.split()
        if (len(words) > 1) and (any(x in words for x in award_words)):
          awards_list.append(award_name)

    global award_dict
    most_common_awards = Counter(awards_list).most_common((len(award_dict)))

    awards = [x[0] for x in most_common_awards]
    return awards

def get_nominees(year):
    '''Nominees is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change
    the name of this function or what it returns.'''
    global table
    if table is None:
        pre_ceremony(year)

    print("\nGetting the nominees for each award category...")
    global award_dict
    nominees = {}
    for a in award_dict:
        nominees[a] = {}
    return nominees

def get_winner(year):
    '''Winners is a dictionary with the hard coded award
    names as keys, and each entry containing a single string.
    Do NOT change the name of this function or what it returns.'''
    winners = {}
    global table
    if table is None:
        pre_ceremony(year)

    print("\nGetting the winners for each award category...")
    global award_dict
    for award in award_dict:
        candidate_tweets = award_tweets(table,award,['win'])
        if 'performance' in award_dict[award]:
            winner_tweets = " ".join(candidate_tweets) #merge to one string
            winner_tweets = re.sub(r'\b%s\b' % 'Golden Globes|Motion|Picture|Performance|Best', '', winner_tweets) #Remove the term Golden Globes
            ngram_counts = Counter(ngrams(winner_tweets.split(), 2)) #Create list of bigrams
            top_bigrams = ngram_counts.most_common(10) #Find top 10
            names = [bigram[0][0]+' '+bigram[0][1] for bigram in top_bigrams if bigram[0][0][0].isupper() and bigram[0][1][0].isupper()] #Filter out bigrams that aren't both capitalized
            #print(award)
            #print(names)

    winners = {}
    for a in award_dict:
        winners[a] = {}
    return winners


def get_presenters(year):
    presenter_keywords = ['present']
    presenters = {}

    global table
    if table is None:
        pre_ceremony(year)

    print("\nGetting the presenters for each award category...")
    global award_dict
    for award in award_dict:
        filtered_tweets = award_tweets(table,award,presenter_keywords)
        presenter_tweets = " ".join(filtered_tweets)
        presenter_tweets = re.sub(r'\b%s\b' % 'GoldenGlobes|Golden Globes|Motion|Picture|Performance|Best', '', presenter_tweets)
        extracted_names = extract_people(presenter_tweets)
        presenter_names_ngrams_counter = Counter(extracted_names)
        top_bigrams = presenter_names_ngrams_counter.most_common(2)
        presenter_names = [b[0] for b in top_bigrams]

        presenters[award] = presenter_names
    return presenters

def get_redcarpet(year):
    global table
    if table is None:
        pre_ceremony(year)

    print("\nGetting the top five most discussed people from the red carpet...")
    filtered_tweets = table.loc[(table['text'].str.contains("redcarpet|red carpet|Red Carpet", regex=True))]['text']

    string = " ".join(filtered_tweets)
    string = re.sub(r'\b%s\b' % 'Golden Globes|carpet|Carpet|red|Red|redcarpet', '', string)
    most_discussed = extract_people(string)
    best_ngram_counts = Counter(most_discussed).most_common(5)
    most_discussed = [x[0] for x in best_ngram_counts]
    return most_discussed

def get_best_dressed(year):
    global table
    if table is None:
        pre_ceremony(year)

    print("\nGetting the top five best dressed names...")
    filtered_best_dress = table.loc[(table['text'].str.contains("gorgeous|beautiful|amazing dress|best dressed|bestdressed|great outfit|looks great", regex=True))]['text']

    best_dress_tweets = " ".join(filtered_best_dress) #merge to one string
    best_dress_tweets = re.sub(r'\b%s\b' % 'Golden Globes|Best Dressed|Photo|Photos|Best|Dress|Fashion|The|This|Hollywood', '', best_dress_tweets)
    best_names = extract_people(best_dress_tweets)

    best_ngram_counts = Counter(best_names)
    top_best_bigrams = best_ngram_counts.most_common(5) #Find top 5
    best_dressed_names = [bigram[0] for bigram in top_best_bigrams]
    return best_dressed_names

def get_worst_dressed(year):
    global table
    if table is None:
        pre_ceremony(year)

    print("\nGetting the top five worst dressed names...")
    filtered_worst_dress = table.loc[(table['text'].str.contains("worstdressed|worst dressed|worst outfit|bad fashion|worst attire|bad outfit|worst outfit", regex=True))]['text']
    worst_dress_tweets = " ".join(filtered_worst_dress) #merge to one string
    worst_dress_tweets = re.sub(r'\b%s\b' % 'Golden Globes|Worst Dressed|Photo|Photos|Worst|Dress|Fashion|The|This|Hollywood', '', worst_dress_tweets)
    worst_names = extract_people(worst_dress_tweets)

    worst_ngram_counts = Counter(worst_names) #Create list of bigrams
    top_worst_bigrams = worst_ngram_counts.most_common(5) #Find top 5
    worst_dressed_names = [bigram[0] for bigram in top_worst_bigrams]

    return worst_dressed_names

#https://tim.mcnamara.nz/post/2650550090/extracting-names-with-6-lines-of-python-code
def extract_people(text):
    names = []
    for sent in nltk.sent_tokenize(text):
        for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
            if hasattr(chunk, 'label') and chunk.label() == "PERSON":
                name = ' '.join(c[0] for c in chunk.leaves())
                #print(chunk.label(), name)
                names.append(name)
    return names

def pre_ceremony(year):
    '''This function loads/fetches/processes any data your program
        will use, and stores that data in your DB or in a json, csv, or
        plain text file. It is the first thing the TA will run when grading.
        Do NOT change the name of this function or what it returns.'''

    print("Reading in data...")
    data = []
    if year == "2013":
      with open('gg2013.json') as f:
        data = json.load(f)

    elif year == "2015":
      with open('gg2015.json') as f:
        data = json.load(f)

    elif year == "2018":
      with open('gg2018.json') as f:
        data = json.load(f)

    elif year == "2019":
      with open('gg2019.json') as f:
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

    global table
    table = pd.DataFrame({'text':text,'timestamp':timestamp,'user_id':user_id,'user_screen_name':screen_name},index=Id)
    table.index.rename('id',inplace=True)

    global award_dict
    award_dict = []
    if year == "2013" or year == "2015":
        award_dict = award_dictionary("2013")
    elif year == "2018" or year == "2019":
        award_dict = award_dictionary("2018")

    return

def main():
    '''This function calls your program. Typing "python gg_api.py"
    will run this function. Or, in the interpreter, import gg_api
    and then run gg_api.main(). This is the second thing the TA will
    run when grading. Do NOT change the name of this function or
    what it returns.'''


    outer_loop = 1
    while (outer_loop == 1):
        year = input("Which year would you like to know about? ")
        year = year.strip()
        if year == "2013" or year == "2015" or year == "2018" or year == "2019":
            inner_loop = 1
            while (inner_loop == 1):
                print("What information would you like to know? ")
                print ("\n1. Hosts\n2. Awards\n3. Nominees\n4. Winners\n5. Presenters\n6. Best Dressed\n7. Worst Dressed\n8. Red Carpet - Most Discussed\n")
                user_input = input("Choose an option: ")
                user_input = user_input.strip()

                if user_input == "1":
                    print('\n'.join(get_hosts(year)) + "\n")

                elif user_input == "2":
                    print('\n'.join(get_awards(year)) + "\n")

                elif user_input == "3":
                    print("\nNot implemented.")

                elif user_input == "4":
                    print("\nNot implemented.")

                elif user_input == "5":
                    presenters = get_presenters(year)
                    for a in presenters:
                        print(a + " : \n" + '\n'.join(presenters[a]) + "\n")

                elif user_input == "6":
                    print('\n'.join(get_best_dressed(year)) + "\n")

                elif user_input == "7":
                    print('\n'.join(get_worst_dressed(year)) + "\n")

                elif user_input == "8":
                    print('\n'.join(get_redcarpet(year)) + "\n")

                else:
                    print("Invalid input.")

                cont = input("Would you like to continue with this current year? y/n: ")
                if cont.lower() == 'y':
                    continue
                elif cont.lower() == 'n':
                    print("Exiting out of current year.")
                    inner_loop = -1
                    break
                else:
                    print("Invalid input.")
        else:
            print("Information about that year is not available. Please try again.")
            continue

        cont = input("Finish program? y/n: ")
        if cont.lower() == 'n':
            continue
        elif cont.lower() == 'y':
            print("Program finished.")
            outer_loop = -1
            break
        else:
            continue

    return

if __name__ == '__main__':
    #fill_res_dict("2013")
    main()
