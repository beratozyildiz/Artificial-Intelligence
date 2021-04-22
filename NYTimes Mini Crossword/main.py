from utilities import *
from gui_tool import *
from puzzle_tool import *
import pickle

single_stepping = True

a_file = open("puzzles.pkl", "rb")
output = pickle.load(a_file)
a_file.close()

#17/12/2020
# domain = {"1A": ['VERY', 'RARE', 'LEAF', 'HOPE', 'LOVE', 'CATS', 'WHAT', 'HERE', 'FILE', 'CASE', 'WITH', 'THIS', 'GOOD', 'LUCK', 'THAT', 'EACH', 'LIFE', 'BEST', 'BOOK', 'MOST', 'FILM', 'WILL', 'JULY', 'KNOW', 'FULL', 'DOES', 'MEAN', 'MORE', 'CLUB', 'SUIT', 'CARD', 'LIKE', 'SEND', 'HELP', 'USED', 'MANY', 'SAYS', 'HAVE', 'YOUR', 'HOLY', 'WHEN', 'GODS', 'HATS', 'HEAD', 'GEAR', 'THEN', 'FIND', 'ONCE', 'NICE', 'DARK', 'TIED', 'SAME', 'FOUR', 'FIVE', 'WAVE', 'LINE', 'FROM', 'DEAL', 'LOST'],
# "5A": ['ALSO', 'WITH', 'RAIL', 'OAHU', 'MAUI', 'MARK', 'LORI', 'TOWN', 'KNOW', 'STOP', 'THIS', 'PAGE', 'CITY', 'SAFE', 'SNOW', 'CREW', 'THAT', 'WIDE'],
# "6A": ['WISHY', 'WASHY', 'RSVPS', 'RSVPD', 'CASES', 'THEIR', 'WHICH', 'AGREE', 'ASKED', 'GOING', 'BEING', 'ABOUT', 'WORDS', 'SOUND', 'ICYMI', 'ALEXA', 'TOBEL', 'MAYBE', 'RIGHT', 'VIEWS', 'POWER', 'GIRLS', 'HYNES', 'SHARE', 'VISIT', 'COMES'],
# "7A": ['DATA', 'NAME', 'YOUR', 'MOST', 'USED', 'YORK', 'TIME', 'ONCE', 'FROM', 'BEEN', 'LIFE', 'LOVE', 'WALK', 'VERB', 'POPE', 'WELL', 'JUST', 'HAVE', 'HALF', 'LOOK', 'INTO', 'WITH', 'UPON', 'HARD', 'BIRD', 'SURE', 'BUUR', 'MAKE', 'WHEN', 'RANG', 'YEAR', 'MOVE', 'SOME', 'THAT', 'WERE', 'MORE', 'HILL', 'CITY', 'WEEK', 'GIVE', 'INFO', 'REAL', 'LAST', 'FOOD', 'TRIO', 'NUTS', 'ISBN', 'FAST', 'EACH', 'SAME', 'TASK', 'DOES', 'FORM', 'THEY', 'HOUR', 'WILL', 'JOHN', 'LAWN', 'OPEN', 'WANT', 'WONT', 'WORK', 'GAME', 'WORN', 'ALSO', 'EVEN', 'MIND', 'FELL', 'NEWS', 'APPS', 'UBER', 'LOST', 'FIND', 'BODY', 'PLAY', 'HERE', 'HANG', 'BARS', 'KIND', 'SAID', 'ONES', 'SEAT', 'BACK', 'GOOD', 'HURT', 'KEEP', 'MANY', 'PICK', 'TOUR', 'MEET', 'INMA', 'GROW', 'SHOW', 'TONY', 'WORD'],
# "8A": ['KARL', 'MARX', 'MOST', 'BORN', 'THIS', 'FROM', 'LIFE', 'WITH', 'GREW', 'MORE', 'SOME', 'SEAN', 'JUNE', 'LAND', 'FACE', 'THAT', 'EVEN', 'YEAR', 'HOLY', 'BOOK', 'VERY', 'ALSO', 'TRUE', 'MANY'],
# "1D": ['FIRST', 'KNOWN', 'CROSS', 'IMAGE', 'CLARA', 'NURSE', 'UNION', 'CIVIL', 'TRAIT', 'WOULD', 'VISIT', 'WOMAN', 'CLERK', 'ASKED', 'LATIN', 'WHICH', 'MEANS', 'COULD', 'FIELD', 'TODAY', 'ABOUT', 'PHONE', 'YEARS', 'TIMES', 'GREAT', 'STUDY', 'LEVEL', 'SANTA', 'LEARN', 'WATCH', 'YOUVE', 'BEGAN', 'AFTER', 'DAVID', 'LATER', 'WORLD', 'JAPAN', 'ARMED'],
# "2D": ['THREE', 'CRUST', 'DENSE', 'EARTH', 'WAVES', 'GASES', 'UPPER', 'INNER', 'SOLID', 'LARGE', 'AREAS', 'ABOVE', 'LAYER', 'BELOW', 'OUTER', 'OTHER', 'RIGID', 'BASED', 'MAKES', 'GRADE', 'PLATE', 'ONION', 'STUDY', 'VIDEO'],
# "3D": ['FOODS', 'WOULD', 'IMAGE', 'BLACK', 'CREAM', 'WHEAT', 'GOPRO', 'YOUVE', 'DITCH', 'AVOID', 'MEATS', 'THEIR', 'ITEMS', 'HONEY', 'BRAND', 'BEING', 'BASED', 'PLACE', 'LEAVE', 'UNTIL', 'FULLY', 'FUSER', 'CLOSE', 'COVER', 'WIPER', 'MOVES', 'OTHER', 'STEPS', 'COLOR', 'LASER', 'TESCO', 'SKILL', 'JOSES', 'MEANT', 'THINK', 'FIRST', 'EXTRA', 'THESE', 'HEAVY'],
# "4D": ['NOV', 'AGO', 'THE', 'AND', 'SIX', 'JUL', 'HAS', 'ONE', 'TWO', 'SHE', 'FOR', 'ARE', 'AUG', 'BEE', 'ITS', 'YOU', 'KEY', 'WAS', 'BBC', 'MAN', 'DEC', 'CAN', 'FLY', 'PER', 'GOT', 'BUT', 'JUN', 'HAD', 'JAN', 'APR', 'OUT', 'SET'],
# "6D": ['MAY', 'AND', 'MOM', 'CBS', 'SEP', 'THE', 'FOR', 'NOV', 'NOT', 'ONE', 'AUG', 'SET', 'ANN', 'HIT', 'ARE', 'TWO', 'NEW', 'ITS', 'WAS', 'BUT', 'WHO', 'HOW', 'SHE', 'AIR', 'HAS', 'HAD', 'HER']}

#17/11/2020
# domain = {"1A": ['FEB', 'THE', 'FAR', 'CRY', 'NEW', 'FEW', 'YOU', 'GET', 'OFF', 'CAN', 'JUL', 'HOW', 'ITS', 'SEP', 'PUT', 'OWN', 'AND', 'BIT', 'HER', 'JUN', 'HES', 'BUT', 'SAY', 'HAS', 'APR', 'GYM', 'AUG', 'WHO', 'MAY', 'DEC', 'ALL', 'NOT', 'JAN', 'OUT', 'HAD', 'GOT', 'NOV', 'WHY', 'YET', 'WAY', 'HIM', 'ARE', 'WAS', 'FOR', 'SEE', 'OCT', 'LOT', 'SHE', 'RUN', 'YES', 'AGE', 'MIT', 'PAW', 'PSW'],
# "4A": ['ALSO', 'WHEN', 'TILT', 'ONCE', 'EACH', 'THAT', 'JUNE', 'DAYS', 'ADDS', 'LEAP', 'DATE', 'JUMP', 'YOUR', 'WAIT', 'FIND', 'PLUS', 'THEY', 'MOST', 'YEAR', 'PEAK', 'SUNS', 'REST', 'UPON', 'THIS', 'FROM', 'DOES', 'RISE', 'EAST', 'SETS', 'WEST', 'HERE', 'WELL', 'HAVE', 'TIME', 'POLE', 'REAL', 'HEAT', 'COME', 'JULY', 'LAST', 'INTO', 'FOUR', 'SEEM', 'ELUL', 'YULE', 'LENT', 'APEX', 'GALA', 'ADAR', 'FAST', 'MEND', 'NEAP', 'OPEN'],
# "5A": ['TRIAL', 'SCOTT', 'TEXAS', 'IMAGE', 'WENLI', 'HOUSE', 'PARTY', 'ITEMS', 'BELOW', 'TAHOE', 'PLATE', 'TWICE', 'TIMES', 'PIXEL', 'COULD', 'COMES', 'PRICE', 'STORE', 'THERE', 'NEXUS', 'PHONE', 'WOULD', 'FIELD', 'LOWER', 'SEEMS', 'THEIR', 'MOVED', 'CAUSE', 'ENTRY', 'TESTS', 'WOMEN', 'THESE', 'CARRY', 'RISKS', 'WATCH', 'BRADY', 'BEARS', 'TAMPA', 'NIGHT', 'FINAL', 'DRIVE', 'THREW', 'SUITS', 'AGAIN', 'AFTER', 'YEARS', 'COURT', 'SIGNS', 'GOING', 'DRAMA', 'SHOWS', 'CABLE', 'CLICK', 'LIKES', 'ABBOT', 'ADAGE', 'AGAPE', 'AIMED', 'AMENT', 'ANGER', 'ANGLE', 'ANGRY', 'ARCUS', 'ARISE'],
# "6A": ['AUTO', 'ADAM', 'OLDS', 'DOWN', 'KARL', 'CLUE', 'HAVE', 'TIME', 'TECH', 'MAIL', 'HURT', 'NAME', 'MALE', 'ITEM', 'ROBE', 'HOME', 'STTC', 'CODE', 'WITH', 'MOST', 'NEAR', 'MANY', 'BEEN', 'LONG', 'LIKE', 'FORD', 'DEAD', 'FREE', 'ONLY', 'MADE', 'MASS', 'GOLD', 'FROM', 'SWIM', 'BENZ', 'OPEL', 'JACK', 'BRAG', 'CALL', 'COIN', 'GIVE', 'HALF', 'LOCK', 'SKIP', 'SLOT', 'DROP', 'CLUB', 'EXEC', 'HOLD', 'LOST', 'SELL', 'AIRS', 'AWAY', 'BACK', 'BASE', 'BEAN', 'BIST', 'BLOW', 'BOND', 'BUCK', 'BURN', 'BUST', 'CHIT', 'COME', 'COOL'],
# "7A": ['APR', 'ANY', 'THE', 'AIR', 'FOR', 'COD', 'JUL', 'ONE', 'TWO', 'AND', 'END', 'WAS', 'PUT', 'PLY', 'HAS', 'ALL', 'TOP', 'HER', 'USE', 'SEE', 'BUY', 'FIT', 'SHE', 'GOT', 'JUN', 'YOU', 'CAN', 'NOT', 'WET', 'POR', 'CNA', 'PAN', 'MAT', 'HAT', 'CAP', 'INK', 'PAD'],
# "1D": ['GRADY', 'OFTEN', 'FEELS', 'ROADS', 'YOURE', 'CREWS', 'AFTER', 'HEAVY', 'TURNS', 'CALLS', 'LAYER', 'CHIEF', 'SPOTS', 'GIANT', 'TRACK', 'WHICH', 'KNOWN', 'LEADS', 'MUDDY', 'UNTIL', 'THREE', 'BUMPY', 'TIMES', 'DRIVE', 'COAST', 'BLAST', 'ABOUT', 'BASIC', 'THUMB', 'THERE', 'SCENE', 'TRAIL', 'THINK', 'PAVED', 'AWAIT', 'WOULD', 'MILES', 'PARTS', 'TERMS', 'EARTH', 'CLASS', 'DEATH', 'WATER', 'RURAL', 'RAINS', 'THESE', 'SLEET', 'CLIMB', 'GRADE', 'CITED', 'THEIR', 'CLOSE', 'TOWNS', 'HOPES', 'STAFF', 'MAKES', 'SENSE', 'LARGE', 'RUTTY', 'SCOUR', 'PITCH', 'ROUGH', 'FERRY', 'RINSE', 'SWEEP', 'SLACK', 'DIRTY', 'SCRUB', 'STEAM', 'CLEAN', 'DUSTY', 'OILED', 'STORM'],
# "2D": ['WILL', 'USED', 'THAT', 'SAID', 'LOVE', 'WISH', 'MORE', 'THEM', 'CANT', 'FROM', 'MANY', 'HAVE', 'INTO', 'LATE', 'THEY', 'READ', 'ABLE', 'BILL', 'FAKE', 'WHAT', 'MVMS', 'FAST', 'ALSO', 'GIVE', 'BACK', 'FORM', 'TELL', 'DIME', 'GOLD', 'WELL', 'JOHN', 'FEED', 'SIZE', 'THIS', 'PAGE', 'FOOD', 'PART', 'WEVE', 'SEEN', 'WITH', 'LIKE', 'ONCE', 'WERE', 'REAL', 'CASH', 'ONLY', 'VEND', 'SLOT', 'COLA', 'SLUG', 'COIL', 'BIST', 'BUST', 'TOLL', 'KITE', 'BOLT', 'GATE', 'LOAD', 'SHOP', 'HAYS', 'LIST', 'SALE', 'SOLD', 'TURN', 'VENT', 'SIGN', 'CORE'],
# "3D": ['JAN', 'THE', 'PEN', 'ITS', 'DID', 'HIS', 'FUN', 'AND', 'YOU', 'CAN', 'SEP', 'GOT', 'APR', 'FOR', 'SAY', 'NOT', 'MAY', 'MAN', 'ALL', 'WHO', 'WAS', 'SEE', 'MAR', 'AGE', 'CRM', 'NEW', 'BUY', 'NOV', 'NYT', 'SUM', 'HAS', 'USE', 'JUN', 'JUL', 'ONE', 'ESP', 'ACT', 'EAR', 'TAX', 'AGO', 'OIL', 'IRE', 'LIE', 'ACE', 'AIR', 'ALE', 'ARE', 'BAR', 'BAT', 'BIT', 'COB', 'DAY', 'DIE', 'DNA', 'ELK', 'EMU', 'END'],
# "4D": ['MOST', 'SAID', 'SOON', 'KNOW', 'MORE', 'HUNT', 'HAVE', 'WITH', 'THAT', 'WONT', 'MADE', 'THIS', 'TIME', 'RYAN', 'JOEL', 'PREZ', 'LADY', 'TEAM', 'SICK', 'GARY', 'WILL', 'GONE', 'PAST', 'WHAT', 'MAKE', 'ONLY', 'PLAN', 'GIVE', 'CITY', 'FROM', 'JACK', 'MOOD', 'COME', 'AIMS', 'THEY', 'THAN', 'JUST', 'GOOD', 'INTO', 'NEXT', 'WEEK', 'PARK', 'AGED', 'DONE', 'RAJA', 'OMPU', 'PASS', 'EVEN', 'HALF', 'HOUR', 'HELD', 'WIFE', 'VICE', 'JILL', 'NEED', 'PATH', 'DOUG', 'TURN', 'BEST', 'WEVE', 'YOUR', 'BILL', 'BUSH', 'READ', 'LIFE', 'IOWA', 'ONCE', 'LIKE', 'ROSE', 'KTLA', 'NEWS', 'MIKE', 'OVER', 'PLEA', 'VERY', 'WERE', 'THEN', 'JOBS', 'LAST', 'HAND', 'SLIP', 'ABEL', 'RIDE', 'FAST', 'TEME', 'TERM', 'BESS', 'EDEN', 'ADAM', 'BACK', 'AWAY', 'CLAS'],
# "5D": ['JOE', 'THE', 'AND', 'JAN', 'ITS', 'CAR', 'ALL', 'ONE', 'ARE', 'YOU', 'FEW', 'SEP', 'SET', 'FEB', 'CAN', 'BIT', 'WAY', 'GET', 'OUT', 'FOR', 'BOX', 'BUT', 'NOV', 'MAN', 'DAY', 'AGO', 'DER', 'USA', 'TOP', 'HAS', 'ETC', 'GEE', 'NEW', 'ANY', 'USE', 'JUL', 'BOP', 'JUN', 'EAR', 'HIT', 'ESA', 'QUE', 'LAS', 'RAG', 'FLY', 'ZIP', 'OLD', 'AIR', 'CUT', 'ESE', 'FIT', 'RAP', 'DIM', 'BAD', 'BAF', 'BAT', 'BSD', 'FAN', 'FAT', 'FIX']}


#04/11/2020 ---> 0 correct on grid
#05/11/2020 ---> 0 correct on grid (4 in domain --> REGAL, FRETS, SCARF, EFLAT)
#08/11/2020 ---> 6 correct on grid
#10/11/2020 ---> 3 correct on grid (6 in domain)
#12/11/2020 ---> 10 correct on grid (9 in domain --> SSE not found)
#13/11/2020 ---> 7 correct on grid
#15/11/2020 ---> 0 correct on grid (5 in domain --> DAY, BOISE, ASIA, BARK, ODIE)
#16/11/2020 ---> 10 correct on grid (8 in domain --> POINT, SITE not found)
#17/11/2020 ---> 0 correct on grid (7 in domain) !
#18/11/2020 ---> 3 correct on grid (6 in domain --> AMID,QUAKE,DIES,LIKES not found)
#19/11/2020 ---> 10 correct on grid (8 in domain)
#20/11/2020 ---> 10 correct on grid (9 in domain --> Noobs not found)
#22/11/2020 ---> 0 correct on grid (5 in domain --> SOFIA,ATOMS,SLEEP,SAKS,ASAP)
#23/11/2020 ---> 7 correct on grid (8 in domain --> HERE,AFEW not found)
#24/11/2020 ---> 7 correct on grid (8 in domain --> STATE,TWEEN not found)
#25/11/2020 ---> 8 correct on grid (8 in domain --> CDS,KEY not found)
#26/11/2020 ---> 7 correct on grid (8 in domain --> EATUP,DEPT not found)
#27/11/2020 ---> 10 correct on grid (10 in domain)
#29/11/2020 ---> 1 correct on grid (7 in domain --> HAHA, IHEAR, GAS not found)
#30/11/2020 ---> 10 correct on grid (9 in domain --> LOPED not found)


#13/12/2020 ---> 7 correct on grid 
#14/12/2020 ---> 0 correnct on grid

#download puzzle info
# puzzle_info = download_puzzle(single_stepping)
puzzle_info = output["30/11/2020"]

#construct puzzle object
puz = puzzle(puzzle_info,single_stepping)

#uncomment 71-79 if search results are ready
# for word in puz.words.keys():
#     unique_list = []
#     for x in domain[word]: 
#         y = x.upper()
#         # check if exists in unique_list or not 
#         if y not in unique_list: 
#             unique_list.append(y) 

#     puz.words[word].assign_word_domain(unique_list)



#search clues via google api and datamuse api   
puz.search_clues()

#populate grid from domains
puz.solve()

#display the result
puz.create_display(single_stepping) 