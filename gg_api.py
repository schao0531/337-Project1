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


########################################################################################################
# HOST FUNCTIONS
########################################################################################################

def get_hosts(year):
    '''Hosts is a list of one or more strings. Do NOT change the name
        of this function or what it returns.'''

    global table
    pre_ceremony(year)

    print("\nGetting the ceremony hosts...")
    filtered_tweets = table.loc[(table['text'].str.contains('host|Host', regex=True)) & ~(table['text'].str.contains('next|Next', regex=True)) ]['text'] #contains word host, does not contain next
    host_tweets = " ".join(filtered_tweets) #merge to one string
    host_tweets = re.sub(r'\b%s\b' % 'Golden Globes', '', host_tweets) #Remove the term Golden Globes
    ngram_counts = Counter(ngrams(host_tweets.split(), 2)) #Create list of bigrams
    top_bigrams = ngram_counts.most_common(10) #Find top 10
    names = [bigram[0][0]+' '+bigram[0][1] for bigram in top_bigrams if bigram[0][0][0].isupper() and bigram[0][1][0].isupper()] #Filter out bigrams that aren't both capitalized
    return names

########################################################################################################
# AWARD FUNCTIONS
########################################################################################################

def get_awards(year):
    '''Awards is a list of strings. Do NOT change the name
        of this function or what it returns.'''
    # global table
    # if table is None:
    #     pre_ceremony(year)

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

########################################################################################################
# GET NOMINEES FUNCTIONS
########################################################################################################

def get_nominees(year):
    '''Nominees is a dictionary with the hard coded award
        names as keys, and each entry a list of strings. Do NOT change
        the name of this function or what it returns.'''
    # global table
    # if table is None:
    #     pre_ceremony(year)

    print("\nGetting the nominees for each award category...")
    global award_dict
    nominees = {}
    for a in award_dict:
        nominees[a] = {}
    return nominees

########################################################################################################
# WINNER FUNCTIONS
########################################################################################################

def grab_human_winners(tagged_list):
    names = []
    for i in range(len(tagged_list)-2):
        first = tagged_list[i]
        second = tagged_list[i+1]
        third = tagged_list[i+2]
        if first[1] == 'NNP' and second[1] == 'NNP' and ('win' in third[0] or 'won' in third[0]):
            names.append(first[0]+' '+second[0])
    return names

def grab_work_winners(string):
    words = string.split('"')
    if len(words) == 1:
        return []
    elif len(words[1]) < 15:
        return [words[1]]
    else:
        return []

def grab_nonhuman_winners(string):
    names = []
    words = list(filter(None, string.split(' ')))
    for i in range(len(words)-3):
        first = words[i]
        second = words[i+1]
        third = words[i+2]
        fourth = words[i+3]
        if first[0].isupper() and second[0].isupper() and third[0].isupper() and ('win' in fourth or 'won' in fourth):
            names.append(first+' '+second+' '+third)
        elif second[0].isupper() and third[0].isupper() and ('win' in fourth or 'won' in fourth):
            names.append(second+' '+third)
        elif third[0].isupper() and ('win' in fourth or 'won' in fourth):
            names.append(third)
    return names

def relevance_score(string,award):
    return sum([1 for word in award_dict[award] if word in string.lower()])

def tokenize_and_tag(string):
    text = nltk.word_tokenize(string)
    tagged_list = nltk.pos_tag(text)
    return tagged_list

def get_winner(year):
    '''Winners is a dictionary with the hard coded award
        names as keys, and each entry containing a single string.
        Do NOT change the name of this function or what it returns.'''
    # global table
    # if table is None:
    #     pre_ceremony(year)
    print("\nGetting the winners for each award category...")
    winner_table = table.loc[table['text'].str.contains('wins')][['text']]
    winner_table['tagged_list'] = winner_table['text'].map(lambda x: tokenize_and_tag(x))
    winners = {}
    global award_dict
    for award in award_dict:
        candidate_names = []
        winner_table['relevance_score'] = winner_table['text'].map(lambda x: relevance_score(x, award))
        target_score = winner_table['relevance_score'].max()
        while candidate_names == []:
            candidate_table = winner_table.loc[winner_table['relevance_score'] == target_score]
            for col, row in candidate_table.iterrows():
                if 'performance' in award or 'director' in award or 'artist' in award:
                    names = grab_human_winners(row['tagged_list'])
                elif 'series' in award or 'film' in award or 'score' in award or 'song' in award or 'album' in award:
                    names = grab_work_winners(row['text'])
                else:
                    names = grab_nonhuman_winners(row['text'])
                for name in names:
                    candidate_names += names

            if candidate_names == []:
                target_score = target_score - 1
            else:
                top_candidate = Counter(candidate_names).most_common()[0][0]
        winners[award] = top_candidate
    return winners

########################################################################################################
# PRESENTER FUNCTIONS
########################################################################################################

def keyword_present(tweet,keywords):
    for keyword in keywords:
        if keyword.lower() in tweet.lower():
            return True
    return False

def award_tweets(table,award,keywords):
    relevant_tweets = [tweet for tweet in table['text'] if keyword_present(tweet,keywords)]
    high_score = max([(sum([1 for word in award_dict[award] if word in tweet.lower()])) for tweet in relevant_tweets])
    win_candidates = [tweet for tweet in relevant_tweets if sum([1 for word in award_dict[award] if word in tweet.lower()]) == high_score]
    return win_candidates

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

def get_presenters(year):
    presenter_keywords = ['present']
    presenters = {}

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

########################################################################################################
# RED CARPET FUNCTIONS
########################################################################################################

def get_redcarpet(year):
    # global table
    # if table is None:
    #     pre_ceremony(year)

    print("\nGetting the top five most discussed people from the red carpet...")
    filtered_tweets = table.loc[(table['text'].str.contains("redcarpet|red carpet|Red Carpet", regex=True))]['text']

    string = " ".join(filtered_tweets)
    string = re.sub(r'\b%s\b' % 'Golden Globes|carpet|Carpet|red|Red|redcarpet', '', string)
    most_discussed = extract_people(string)
    best_ngram_counts = Counter(most_discussed).most_common(5)
    most_discussed = [x[0] for x in best_ngram_counts]
    return most_discussed

def get_best_dressed(year):
    # global table
    # if table is None:
    #     pre_ceremony(year)

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
    # global table
    # if table is None:
    #     pre_ceremony(year)

    print("\nGetting the top five worst dressed names...")
    filtered_worst_dress = table.loc[(table['text'].str.contains("worstdressed|worst dressed|worst outfit|bad fashion|worst attire|bad outfit|worst outfit", regex=True))]['text']
    worst_dress_tweets = " ".join(filtered_worst_dress) #merge to one string
    worst_dress_tweets = re.sub(r'\b%s\b' % 'Golden Globes|Worst Dressed|Photo|Photos|Worst|Dress|Fashion|The|This|Hollywood', '', worst_dress_tweets)
    worst_names = extract_people(worst_dress_tweets)

    worst_ngram_counts = Counter(worst_names) #Create list of bigrams
    top_worst_bigrams = worst_ngram_counts.most_common(5) #Find top 5
    worst_dressed_names = [bigram[0] for bigram in top_worst_bigrams]

    return worst_dressed_names

########################################################################################################
# PREP FUNCTIONS
########################################################################################################

def stopword_filter(string):
    stop_words = ['i','me','my','myself','we','our','ours','ourselves','you','your','yours','yourself','yourselves','he','him','his','himself','she','her','hers','herself','it','its','itself',
                  'they','them','their','theirs','themselves','what','which','who','whom','this','that','these','those','am','is','are','was','were','be','been','being','have','has','had','having',
                  'do','does','did','doing','a','an','the','and','but','if','or','because','as','until','while','of','at','by','for','with','about','against','between','into','through','during',
                  'before','after','above','below','to','from','up','down','in','out','on','off','over','under','again','further','then','once','here','there','when','where','why','how','all',
                  'any','both','each','few','more','most','other','some','such','no','nor','not','only','own','same','so','than','too','very','s','t','can','will','just','don','should','now','-']
    return ' '.join([w for w in string.split(' ') if not w.lower() in stop_words])

def award_dictionary(year):
    if year == '2013' or year == '2015':
        awards = OFFICIAL_AWARDS_1315
    elif year == '2018' or year == '2019':
        awards = OFFICIAL_AWARDS_1819
    Dict = {}
    for award in awards:
        filtered_sentence = stopword_filter(award)
        Dict[award] = filtered_sentence.split(' ')
    return Dict


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

########################################################################################################
# OUTPUT FUNCTION
########################################################################################################

def fill_res_dict(year):
    print("saving year results in a json format...")
    hosts = get_hosts(year)
    awards = get_awards(year)
    nominees = get_nominees(year)
    winners = get_winner(year)
    presenters = get_presenters(year)

    res_dict = {}
    res_dict["hosts"] = hosts

    i = 0

    OFFICIAL_AWARDS = []
    if year == "2013" or year == "2015":
        OFFICIAL_AWARDS = OFFICIAL_AWARDS_1315
    elif year == "2018" or year == "2019":
        OFFICIAL_AWARDS = OFFICIAL_AWARDS_1819

    res_dict["award_data"] = {}
    for award in OFFICIAL_AWARDS:
        res_dict["award_data"][award] = {}
        res_dict["award_data"][award]["parsed_name"] = awards[i]
        res_dict["award_data"][award]["nominees"] = nominees[award]
        res_dict["award_data"][award]["presenters"] = presenters[award]
        res_dict["award_data"][award]["winner"] = winners[award]
        i += 1

    with open('gg%s_studentanswers.json' % year, 'w') as fp:
        json.dump(res_dict, fp)

########################################################################################################
# MAIN
########################################################################################################

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
            pre_ceremony(year)
            while (inner_loop == 1):
                print("What information would you like to know? Type the option's number, eg '4' ")
                print ("\n1. Hosts\n2. Awards\n3. Nominees\n4. Winners\n5. Presenters\n6. Best Dressed\n7. Worst Dressed\n8. Red Carpet - Most Discussed\n")
                user_input = input("Choose an option: ")
                user_input = user_input.strip()

                if user_input == "1":
                    print('\n'.join(get_hosts(year)) + "\n")

                elif user_input == "2":
                    print('\n'.join(get_awards(year)) + "\n")

                elif user_input == "3":
                    nominees = get_nominees(year)
                    for n in nominees:
                        print(n)
                        print(nominees[n],'\n')

                elif user_input == "4":
                    winners = get_winner(year)
                    for winner in winners:
                        print(winner)
                        print(winners[winner],'\n')

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

        cont = input("Exit program? y/n: ")
        if cont.lower() == 'n':
            continue
        elif cont.lower() == 'y':
            save_json = input("Save output to json format? y/n: ")
            if save_json.lower() == 'y':
                fill_res_dict(year)
            print("Program finished.")
            outer_loop = -1
            break
        else:
            continue


if __name__ == '__main__':
    main()
