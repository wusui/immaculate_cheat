# Copyright (C) 2023 Warren Usui, MIT License
"""
Extract team data for each player from the baseball reference website
"""
import sys
import json
import secrets
import time
import pandas as pd
from get_everybody import get_everybody

def equiv():
    """
    Handle older team names
    """
    return {'FLA': 'MIA', 'MON': 'WSN', 'TBD': 'TBR', 'CAL': 'LAA',
            'ANA': 'LAA', 'SEP': 'MIL', 'MLN': 'ATL', 'NYG': 'SFG',
            'SLB': 'BAL', 'BRO': 'LAD', 'WSH': 'MIN', 'PHA': 'OAK',
            'KCA': 'OAK', 'BSN': 'ATL', 'WSA': 'TEX'}

def mlb_tms():
    """
    Team list used to make sure all team names are valid
    """
    return ['BAL', 'TBR', 'TOR', 'NYY', 'BOS', 'ATL', 'PHI', 'MIA', 'NYM',
            'WSN', 'MIN', 'DET', 'CLE', 'CHW', 'KCR', 'MIL', 'CHC', 'CIN',
            'PIT', 'STL', 'HOU', 'TEX', 'SEA', 'LAA', 'OAK', 'LAD', 'ARI',
            'SDP', 'SFG', 'COL']

def read_info(player):
    """
    Extract player information from the baseball reference site
    """
    return pd.read_html(f'https://www.baseball-reference.com{player}')

def pl_teams(player_pd):
    """
    Extracts teams from the last table on the player's webpage
    """
    def pl_in1(pd_row):
        def pl_in2(row_strs):
            def pl_in3(row_tms):
                def pl_in4(tm_only):
                    return list(filter(lambda a: len(a) == 3, tm_only))
                return pl_in4(list(map(lambda a: a.split(' ')[0], row_tms)))
            return pl_in3(list(filter(lambda a: '(' in a, row_strs)))
        return pl_in2(list(filter(lambda a: isinstance(a, str), pd_row)))
    return pl_in1(player_pd[-1].iloc[:, 1].tolist())

def get_pl_teams(player_id):
    """
    Read routine wrapper that delays so that the baseball reference website does not
    shut down on us.
    """
    time.sleep(secrets.randbits(4) + 15)
    print(player_id)
    return pl_teams(read_info(player_id))

def get_all_info():
    """
    Loop through all players, extracting information
    """
    def gai_in1(mlb_teams):
        def gai_in2(equiv_tm):
            def fix_nms(tname):
                if tname in equiv_tm:
                    return equiv_tm[tname]
                return tname
            def all_ok(tname):
                if tname not in mlb_teams:
                    sys.exit(f'{tname} is an invalid team name')
                return tname
            def scrub(tm_list):
                return list(map(all_ok, list(map(fix_nms, tm_list))))
            def gai_in3(pers_data):
                return [pers_data, scrub(get_pl_teams(pers_data))]
            return list(map(gai_in3, get_everybody()))
        return gai_in2(equiv())
    return gai_in1(mlb_tms())

def get_player_teams():
    """
    Stash dictionary in plyr_info.json
    """
    with open('plyr_info.json', 'w', encoding='utf-8') as outfile:
        outfile.write(json.dumps(dict(get_all_info()), indent=4))

if __name__ == "__main__":
    get_player_teams()
