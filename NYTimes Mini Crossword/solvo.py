from googleapiclient.discovery import build
from datamuse import datamuse

#First
my_api_key0 =  "AIzaSyA8gwI2_EAyJPB_s5VjOov52DFxunQUHJI" #The API_KEY you acquired
my_cse_id0 =  "21714045fa03cc7bf" #The search-engine-ID you created

# #SECOND
my_api_key3 =  "AIzaSyAbNMviohZp1kO3dErSDTGJdujHpo_zkFU" #The API_KEY you acquired
my_cse_id3 =  "5c7c592812493a880" #The search-engine-ID you created

#third
my_api_key1 = "AIzaSyA8SvyXFLwXiA3Y3eesZTf9f24YYnjP1w0" #The API_KEY you acquired
my_cse_id1 = "b8e7e205f68568741" #The search-engine-ID you created

#fourth
my_api_key2 =  "AIzaSyBb_xxznvZZFzg4BiNkQ9vw3zKuP9L6baE" #The API_KEY you acquired
my_cse_id2 =  "52834ebca8cacf265" #The search-engine-ID you created

my_api_key = [my_api_key0,my_api_key1,my_api_key2,my_api_key3]
my_cse_id = [my_cse_id0,my_cse_id1,my_cse_id2,my_cse_id3]

api = datamuse.Datamuse()

def google_search(search_term, api_key, cse_id, i, **kwargs):
    try:
        service = build("customsearch", "v1", developerKey=api_key[i])
        res = service.cse().list(q=search_term, cx=cse_id[i], **kwargs).execute()
        if 'items' in res.keys():
            return res['items']
        else:
            return []
    except:
        i += 1
        print(i)
        if i <= 3:
            return google_search(search_term, api_key, cse_id, i)
        else:
            return []



def word_domain(clue, lenght):
    results = google_search(clue, my_api_key, my_cse_id, 0, num=10)

    res = []
    #for result in results:
        #print(result)

    for result in results:
        for word in result['snippet'].split():
            actual_word = ''
            for char in word:
                if char.isalpha():
                    actual_word += char
            if len(actual_word) == lenght:
                res.append(actual_word)
    #print(res)
    return res

def data_muse(clue,length):
    results = api.words(ml=clue)
    
    res = []
    for lst in results:
        word = lst['word']
        if len(word) == length:
            res.append(word)
    
    return res
    