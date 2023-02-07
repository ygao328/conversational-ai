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

transitions = {
    'state': 'start',
    '`Hello, how can I help you?`': {
        '{haircut, hair cut, hair cuts, [cut, hair]}': {
            '`Sure. What date and time are you looking for?`' :{
                '{[monday,10,am], [monday,1,pm], [monday,2,pm], [tuesday,2,pm]}':{
                   '`Your appointment is set. See you!`' :'end'
                },
                'error':{
                    '`Sorry, that slot is not available for a haircut`': 'end'
                },
                    },
        },
        '{[hair, coloring], [color, hair]}': {
            '`Sure. What date and time are you looking for?`': {
                '{[wednesday, 10,am], [wednesday, 11, am], [wednesday,1,pm], [thursday,10,am], [thursday,11, am]}': {
                    '`Your appointment is set. See you!`': 'end'
                },
                'error': {
                    '`Sorry, that slot is not available for a hair coloring`': 'end'
                },
            },

        },
        '{perms, perm}': {
            '`Sure. What date and time are you looking for?`': {
                '{[friday,10, am], [friday, 11, am], [friday, 1, pm], [friday, 2, pm], [saturday, 10, am], [saturday,2, pm]}': {
                    '`Your appointment is set. See you!`': 'end'
                },

                'error': {
                    '`Sorry, that slot is not available for a perms`': 'end'
                },
            },

        },

       'error':  {
           '`Sorry we do not provide that service.`': 'end'

       },
    }
}

df = DialogueFlow('start', end_state='end')
df.load_transitions(transitions)

if __name__ == '__main__':
    df.run()