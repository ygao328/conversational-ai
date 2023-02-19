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
import re

class MacroGetName(Macro):
    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[Any]):
        r = re.compile(r"(.*is|.*called|.*am|.*call me|.*mr|.*mrs|.*ms|.*dr)?(?:^|\s)([a-z']+)(?:\s([a-z']+))?") #adjust for other words in front of name
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
class MacroGetThoughts(Macro):
    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[Any]):
         return True
transitions = {
    'state': 'start',
    '`Hello. What is your name?`': {
        '#GET_NAME': {
            '`It\'s nice to meet you,` $FIRSTNAME `. What was the latest movie you watched?`':{

                '[#ONT(action/adventure)]': {
                    '`I love action/adventure movies. They for sure keep me on my seat. Who is your favorite character?`': {
                        '#GET_CHARACTER':{
                            '`That\'s a good one,` $FIRSTNAME `is so cool. So I guess you really like action movies?`': {
                                '{yes,yeah,[I,do]}':{
                                    '`Awh, cool! Why do you like them so much?`':{
                                        '#GET_THOUGHT':{
                                            "`Thanks for sharing with me. I feel that!`": 'end'
                                        },
                                        'error': {
                                            "`Sorry I don't understand that.`":'end'
                                        },

                                    }

                                },
                                '{no, nope, [I, do, not]}':{ #not sure why don't doesn't work
                                    '`Awh, shucks. Why don\'t you like them?`':{
                                        '#GET_THOUGHT':{
                                            "`Thanks for sharing with me. I feel that!`": 'end'
                                        },
                                        'error': {
                                            "`Sorry I don\'t understand that.`":'end'
                                        },

                                    }

                                },
                                'error':{
                                    "`Oops I don\'t understand that.`":'end'
                                }
                            }
                        }
                    }
                 },
                '[#ONT(drama)]': {
                    '`I love dramas. The complexity of the plot definitely keeps me on my toes. Who is your favorite character?`': {
                        '#GET_CHARACTER': {
                            '`That\'s a good one,` $FIRSTNAME `is so cool. So I guess you really like dramas?`': {
                                '{yes,yeah,[I,do]}': {
                                    '`Awh, cool! Why do you like them so much?`': {
                                        '#GET_THOUGHT': {
                                            "`Thanks for sharing with me. I feel that!`": 'end'
                                        },
                                        'error': {
                                            "`Sorry I don't understand that.`": 'end'
                                        },

                                    }

                                },
                                '{no, nope, [I, do, not]}': {  # not sure why don't doesn't work
                                    '`Awh, shucks. Why don\'t you like them?`': {
                                        '#GET_THOUGHT': {
                                            "`Thanks for sharing with me. I feel that!`": 'end'
                                        },
                                        'error': {
                                            "`Sorry I don\'t understand that.`": 'end'
                                        },

                                    }

                                },
                                'error': {
                                    "`Oops I don\'t understand that.`": 'end'
                                }
                            }
                        }
                    }
                },
                '[#ONT(horror/thriller)]': {
                    '`Yikes, I just can\'t do horror movies. They really freak me out. You\'re a brave one.:) Who is your favorite character?`': {
                        '#GET_CHARACTER': {
                            '`That\'s a good one,` $FIRSTNAME `is so cool. So I guess you really like horror/thriller movies?`': {
                                '{yes,yeah,[I,do]}': {
                                    '`Awh, cool! Why do you like them so much?`': {
                                        '#GET_THOUGHT': {
                                            "`Thanks for sharing with me. I feel that!`": 'end'
                                        },
                                        'error': {
                                            "`Sorry I don't understand that.`": 'end'
                                        },

                                    }

                                },
                                '{no, nope, [I, do, not]}': {  # not sure why don't doesn't work
                                    '`Awh, shucks. Why don\'t you like them?`': {
                                        '#GET_THOUGHT': {
                                            "`Thanks for sharing with me. I feel that!`": 'end'
                                        },
                                        'error': {
                                            "`Sorry I don\'t understand that.`": 'end'
                                        },

                                    }

                                },
                                'error': {
                                    "`Oops I don\'t understand that.`": 'end'
                                }
                            }
                        }
                        }
                 },
                '[#ONT(comedy)]': {
                    '`HAHA I love a good laugh. Comedy based movies always cheer me up. Who is your favorite character?`': {
                        '#GET_CHARACTER': {
                            '`That\'s a good one,` $FIRSTNAME `is so cool. So I guess you really like comedy movies?`': {
                                '{yes,yeah,[I,do]}': {
                                    '`Awh, cool! Why do you like them so much?`': {
                                        '#GET_THOUGHT': {
                                            "`Thanks for sharing with me. I feel that!`": 'end'
                                        },
                                        'error': {
                                            "`Sorry I don't understand that.`": 'end'
                                        },

                                    }

                                },
                                '{no, nope, [I, do, not]}': {  # not sure why don't doesn't work
                                    '`Awh, shucks. Why don\'t you like them?`': {
                                        '#GET_THOUGHT': {
                                            "`Thanks for sharing with me. I feel that!`": 'end'
                                        },
                                        'error': {
                                            "`Sorry I don\'t understand that.`": 'end'
                                        },

                                    }

                                },
                                'error': {
                                    "`Oops I don\'t understand that.`": 'end'
                                }
                            }
                        }
                    }
                 },
                '[#ONT(animation)]': {
                    '`We love a good animation. SLAY! Who is your favorite character?`': {
                        '#GET_CHARACTER': {
                            '`That\'s a good one,` $FIRSTNAME ` is so cool. So I guess you really like animated movies?`': {
                                '{yes,yeah,[I,do]}': {
                                    '`Awh, cool! Why do you like them so much?`': {
                                        '#GET_THOUGHT': {
                                            "`Thanks for sharing with me. I feel that!`": 'end'
                                        },
                                        'error': {
                                            "`Sorry I don't understand that.`": 'end'
                                        },

                                    }

                                },
                                '{no, nope, [I, do, not]}': {  # not sure why don't doesn't work
                                    '`Awh, shucks. Why don\'t you like them?`': {
                                        '#GET_THOUGHT': {
                                            "`Thanks for sharing with me. I feel that!`": 'end'
                                        },
                                        'error': {
                                            "`Sorry I don\'t understand that.`": 'end'
                                        },

                                    }

                                },
                                'error': {
                                    "`Oops I don\'t understand that.`": 'end'
                                }
                            }
                        }
                    }
                 },
                '[#ONT(fantasy)]': {
                    '`OOOOO a fantasy based movie is where it\'s at. How amazing. Who is your favorite character?`': {
                        '#GET_CHARACTER': {
                            '`That\'s a good one,` $FIRSTNAME ` is so cool. So I guess you really like fantasy movies?`': {
                                '{yes,yeah,[I,do]}': {
                                    '`Awh, cool! Why do you like them so much?`': {
                                        '#GET_THOUGHT': {
                                            "`Thanks for sharing with me. I feel that!`": 'end'
                                        },
                                        'error': {
                                            "`Sorry I don't understand that.`": 'end'
                                        },

                                    }

                                },
                                '{no, nope, [I, do, not]}': {  # not sure why don't doesn't work
                                    '`Awh, shucks. Why don\'t you like them?`': {
                                        '#GET_THOUGHT': {
                                            "`Thanks for sharing with me. I feel that!`": 'end'
                                        },
                                        'error': {
                                            "`Sorry I don\'t understand that.`": 'end'
                                        },

                                    }

                                },
                                'error': {
                                    "`Oops I don\'t understand that.`": 'end'
                                }
                            }
                        }
                    }
                 },
                'error': {
                      '`Hmmm. I am not sure if we have anything in common to talk about then. Sorry, but bye.`': 'end'
                }
            }
        },
        'error': {
            '`Sorry, I didn\'t catch your name`': 'end'
        }
    }
}

macros = {
    'GET_NAME': MacroGetName(),
    'GET_CHARACTER': MacroGetCharacter(),
   'GET_THOUGHT': MacroGetThoughts()
}

df = DialogueFlow('start', end_state='end')
df.load_transitions(transitions)
df.knowledge_base().load_json_file('resources/ontology_quiz3.json')
df.add_macros(macros)

if __name__ == '__main__':
    df.run()