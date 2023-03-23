# ========================================================================
# Copyright 2022 Emory University
#
# Licensed under the Apache License, Version 2.0 (the `License`);
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an `AS IS` BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ========================================================================
__author__ = 'Yifei Gao'

from emora_stdm import DialogueFlow
from emora_stdm import Macro, Ngrams
from typing import Dict, Any, List
import pickle
import re


def save(df: DialogueFlow, varfile: str):
    df.run()
    d = {k: v for k, v in df.vars().items() if not k.startswith('_')}
    pickle.dump(d, open(varfile, 'wb'))

def load(df: DialogueFlow, varfile: str):
    d = pickle.load(open(varfile, 'rb'))
    df.vars().update(d)
    df.run()
    save(df, varfile)
class MacroGetName(Macro):
    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[Any]):
        r = re.compile(r"(.*is|.*called|.*am|.*call me|.*mr|.*mrs|.*ms|.*dr)?(?:^|\s)([a-z']+)(?:\s([a-z']+))?") #adjust for other words in front of name
        m = r.search(ngrams.text())
        if m is None: return False

        title, firstname, lastname = None, None, None
        if m.group(1):
            title = m.group(1)
            if m.group(3):
                firstname = m.group(2)
                lastname = m.group(3)
            else:
                firstname = m.group(2)
                lastname = m.group(3)
        else:
            firstname = m.group(2)
            lastname = m.group(3)

        vars['TITLE'] = title
        vars['FIRSTNAME'] = firstname
        vars['LASTNAME'] = lastname

        return True
import time

class MacroTime(Macro):
    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[str]):
        current_time = time.strftime("%H:%M")
        return "{}".format(current_time)
class MacroGetCharacter(Macro):
    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[Any]):
        r = re.compile(r"(.*is|.*be|.*the|.*called|.*am|.*call me|.*mr|.*mrs|.*ms|.*dr)?(?:^|\s)([a-z']+)(?:\s([a-z']+))?") #adjust for other words in front of name
        m = r.search(ngrams.text())
        if m is None: return False

        title, firstname, lastname = None, None, None
       # print(m.group(1)) #everything before the first name
        #print(m.group(2)) #first Name
        #print(m.group(3)) #last Name
        #print(m.group()) #the entire group
        if m.group(1):
            title = m.group(1)
            if m.group(3):
                firstname = m.group(3)
                lastname = m.group(3)
            else:
                firstname = m.group(2)
                lastname = m.group(3)
        else:
            firstname = m.group(2)
            lastname = m.group(3)

        vars['TITLE'] = title
        vars['FIRSTNAME'] = firstname
        vars['LASTNAME'] = lastname
        return True
class MacroGetThoughts(Macro):
    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[Any]):
         return True

import random
class MovieTitle(Macro):
    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[Any]):
        titles = ['The Godfather', 'The Shawshank Redemption', 'The Dark Knight', 'Schindler\'s List', 'Forrest Gump',
                  'The Lord of the Rings: The Return of the King', 'Star Wars: Episode V - The Empire Strikes Back',
                  'Pulp Fiction', 'The Good, the Bad and the Ugly', 'The Lord of the Rings: The Fellowship of the Ring',
                  'Fight Club', 'Inception', 'The Lord of the Rings: The Two Towers', 'The Matrix', 'Goodfellas',
                  'Seven Samurai', 'City of God', 'The Silence of the Lambs', 'It\'s a Wonderful Life',
                  'Life is Beautiful']
        key = 'USEDMOVIETITLES'+ vars['FIRSTNAME']
        if key not in vars.keys():
            vars[key]=[]
        used_titles = vars[key]
        while True:
            random_title = random.choice(titles)
            if random_title not in used_titles:
                used_titles.append(random_title)
                vars['MOVIETITLE'+ vars['FIRSTNAME']]=random_title
                vars[key]=used_titles
                return random_title
class MovieDescription(Macro):
    used_genres = []

    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[Any]):
        genres = ['Crime', 'Drama', 'Action', 'Biography', 'Drama', 'Adventure', 'Action', 'Crime', 'Western',
                  'Adventure', 'Drama', 'Action', 'Adventure', 'Action', 'Biography', 'Action', 'Drama', 'Thriller',
                  'Drama', 'Comedy']

        while True:
            random_genre = random.choice(genres)
            if random_genre not in self.used_genres:
                self.used_genres.append(random_genre)
                return random_genre

class SongTitle(Macro):
    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[Any]):
        song_titles = ['Rolling in the Deep', 'Bohemian Rhapsody', 'Hey Jude', 'Like a Rolling Stone',
                       'I Will Always Love You', 'Imagine', 'What\'s Going On', 'Purple Haze', 'Hotel California',
                       'Billie Jean', 'Stairway to Heaven', 'Hallelujah', 'My Girl', 'Good Vibrations',
                       'Sweet Child O\' Mine',
                       'Thriller', 'Smells Like Teen Spirit', 'Let It Be', 'All Along the Watchtower', 'Born to Run']
        key = 'USEDTITLES' + vars['FIRSTNAME']
        if key not in vars.keys():
            vars[key]=[]
        used_titles = vars[key]
        while True:
            random_title = random.choice(song_titles)
            if random_title not in used_titles:
                used_titles.append(random_title)
                vars['MOVIETITLE'+ vars['FIRSTNAME']] = random_title
                vars[key] = used_titles
                return random_title

class SongDescription(Macro):
    used_artists = []

    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[Any]):
        artists = ['Adele', 'Queen', 'The Beatles', 'Bob Dylan', 'Whitney Houston', 'John Lennon', 'Marvin Gaye',
                   'Jimi Hendrix', 'The Eagles', 'Michael Jackson', 'Led Zeppelin', 'Jeff Buckley', 'The Temptations',
                   'The Beach Boys', 'Guns N\' Roses', 'Michael Jackson', 'Nirvana', 'The Beatles', 'Jimi Hendrix',
                   'Bruce Springsteen']

        while True:
            random_artist = random.choice(artists)
            if random_artist not in self.used_artists:
                self.used_artists.append(random_artist)
                return random_artist

class MacroWhatElse(Macro):
    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[Any]):
      # vn = 'HAVE_TALK'
      # if vn in vars and vars[vn]:
      #  return 'What else do you want me to recommend?'
     #  else:
      #     vars[vn] = True
       # #    return 'What do you want me to recommend?'
        vn = 'MOVIETITLE'+ vars['FIRSTNAME']
       # vn2='SONGTITLE' + vars['FIRSTNAME']

        if vn in vars:
            return 'Did you enjoy the '+ vars[vn]+ ' What else do you want me to recommend?'
       # elif vn2 in vars:
           # return 'Did you enjoy the' + vars[vn2]+' What else do you want me to recommend?'
        else:
            return 'What else do you want me to recommend?'


class Names(Macro):
    used_names = []

    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[Any]):
        questions = [
            "What should I call you?",
            "May I know your name?",
            "What do you like to be called?",
            "Who am I talking to?",
            "What is your given name?",
            "Could you tell me your name?",
            "How should I address you?",
            "What name do you go by?",
            "What's your name?",
            "Can you share your name with me?",
            "What name were you given?",
            "What shall I call you?",
            "What is your title?",
            "May I have your name please?",
            "What is the name you use?",
            "What name do you prefer?",
            "What is the name you were given?",
            "What name do you respond to?",
            "Can I know your name?",
            "What should I call you by?"
        ]

        while True:
            random_title = random.choice(questions)
            if random_title not in self.used_names:
                self.used_names.append(random_title)
                return random_title


transitions = {
    'state': 'start',
    '`Hello. The time is` #TIME #NAME': {
        '#GET_NAME': {
            'state': 'good',
            '`Hi` $FIRSTNAME `.` #WHAT_ELSE': {
                '[#LEM(movie)]': 'movie',
                '[song]': 'song',
                'error': {
                    'state': 'goodbye',
                    '`Goodbye!`': 'end'
                }
            }
        },
        'error': 'goodbye'
    }
}

song_transitions = {
    'state': 'song',
    '`I would recommend `#SONGTITLE`. It is literally my jam.`':{
        '[{about, genre, information, more, [more, information]}]': {
            '`The artist is` #SONGARTIST `. `': 'good'

        },
        '[{thank, thanks, bye}]': {
            '`Enjoy! And Goodbye!`': 'end'
        },

        'error':'good'
    }
}

movie_transitions = {
    'state': 'movie',
    #if this is the first time and there is no issues caught
    '`I would recommend `#MOVIETITLE` It\'s my personal favorite.`': {
        '[{what, more, information, about}]': {
            '`The genre is` #MOVIEGENRE `.`':'good'
        },
        '[{no, thank, thanks, bye}]': {
            '`I think you would like it. Don\'t mention.`':'end'
        },
        'error':'good'
    }


}


macros = {
    'GET_NAME': MacroGetName(),
    'WHAT_ELSE': MacroWhatElse(),
    'TIME': MacroTime(),
    'MOVIETITLE':MovieTitle(),
    'MOVIEGENRE':MovieDescription(),
    'GETTHOUGHT':MacroGetThoughts(),
    'SONGTITLE':SongTitle(),
    'SONGARTIST': SongDescription(),
    'NAME': Names()
}



df=DialogueFlow('start', end_state='end')
df.load_transitions(transitions)
df.load_transitions(song_transitions)
df.load_transitions(movie_transitions)
df.add_macros(macros)

# return df

if __name__ == '__main__':
    load(df, 'resources/visits.pkl')



    #issues are One, I cannot save the progress I am super confused as to how to do that
#two, not sure why the movie genre insides are not matching correctly.
#how do you get rid of Hi its nice to meet you yifei? 