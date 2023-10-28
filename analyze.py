# Copyright (C) 2023 Warren Usui, MIT License
"""
Analyze the best_guesses data
"""
from itertools import chain
from get_player_teams import mlb_tms
from find_candidates import pair_up, get_split, read_json, get_player_tpairs

def analyze(prev_info):
    """
    Make info in best_guesses file more readable
    """
    def find_pairs(solution_17):
        def get_plists():
            return list(map(lambda a: prev_info['player_tpairs'][a],
                            solution_17))
        def chain_plists():
            return sorted(list(set(chain.from_iterable(get_plists()))))
        def chk_all():
            return list(filter(lambda a: a not in chain_plists(),
                               prev_info['all_pairs']))
        def get_team_list():
            return list(chain.from_iterable(list(map(lambda a: a.split('_'),
                                                     chk_all()))))

        return {'player': solution_17, 'odd_teams':
                list(set(get_team_list()))}

    def get_sol_row(sol_row):
        def get_sm_grp(sm_grp):
            return find_pairs(sol_row[0] + sm_grp)
        return list(map(get_sm_grp, sol_row[2]))
    return list(map(get_sol_row, prev_info['in_data']))

if __name__ == "__main__":
    print(analyze({'all_pairs': sorted(pair_up(sorted(mlb_tms()))),
             'player_tpairs': get_player_tpairs(),
             'in_data': read_json(f'best_guesses{get_split()}.json')}))
