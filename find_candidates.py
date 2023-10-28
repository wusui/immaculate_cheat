# Copyright (C) 2023 Warren Usui, MIT License
"""
Look for 18 player solutions
"""
import json
from itertools import combinations, chain

def get_split():
    """
    Players added before trying all combinations.  This value is the number
    of players picked before trying every combination to get the total
    number of players picked up to 17.  14 feels like the lowest value
    that can be set without taking too long to go through all the later
    combinations.
    """
    return 14

def get_pre_picks():
    """
    If non-empty value is returned, only try these players for first
    player loop
    """
    return ['/players/w/wrighja01.shtml', '/players/c/cabreor01.shtml']

def read_json(fname):
    """
    Read in player data
    """
    with open(fname, 'r', encoding='utf-8') as ifd:
        return json.load(ifd)

def pair_up(tlist):
    """
    Convert pairs of team abbreviations into one string
    """
    return list(map('_'.join, list(combinations(tlist, 2))))

def get_player_tpairs():
    """
    Convert dictionary of list of teams to dictionary of list of team pairs
    """
    def pt_inner(pinfo):
        return list(map(lambda a: [a, pair_up(sorted(pinfo[a]))], pinfo))
    return dict(pt_inner(read_json('plyr_info.json')))

def output_json(in_data):
    """
    Save json output generated
    """
    with open(f'best_guesses{get_split()}.json', 'w', encoding='utf-8') \
                    as outfile:
        outfile.write(json.dumps(in_data, indent=4))

def try_to_find_18():
    """
    The main solution finder in this repo.  player_tpairs is a dictionary
    indexed by player whose values are lists of team pairs.  The general
    plan here is to:

    1. Try every player as the first one in the solution.
    2. For the next thirteen players in the solution, select the player that
       causes the unmatched pairs left to decrease the most
    3. With fourteen cards in, try every remaining three card combo, saving
       all times when the remaining unmatched team list has five or fewer
       teams (previous experience has shown that this is likely to happen).

    The expected output will be a list where each entry is a list of two
    items:  The list of people in the solution so far, and a list of
    teams that the eighteenth player needs to have in order for a solution
    to be possible.
    """
    def ttf_inner(player_tpairs):
        def merge_lists(pair_lists):
            return sorted(list(set(list(chain.from_iterable(pair_lists)))))
        def get_tm_list(solution_list):
            return merge_lists(list(map(lambda a: player_tpairs[a],
                                     solution_list)))
        def best_p(solution_list):
            def find_best(list_of_sol):
                def fbin(msize):
                    return list(filter(lambda a: a[1] == msize,
                                       list_of_sol))[0]
                return fbin(max(list(map(lambda a: a[1], list_of_sol))))
            def bp_inner(tm_list):
                return [find_best(list(map(lambda a: [a,
                            len(merge_lists([tm_list, player_tpairs[a]]))],
                            player_tpairs)))[0]]
            return bp_inner(get_tm_list(solution_list))
        def find_next_guy(solution_list):
            if len(solution_list) == get_split():
                return solution_list
            return find_next_guy(solution_list + best_p(solution_list))
        def pick_start(first_player):
            return find_next_guy([first_player])
        def get_team_pairs(players):
            return merge_lists(list(map(lambda a: player_tpairs[a], players)))
        def look_for_3s(this_one_14):
            def pair_list_14(pot_14):
                def combo_not_uniq(combo_3):
                    return list(filter(lambda a: a in this_one_14,
                                        combo_3))
                def check_3combo(combo_3):
                    if combo_not_uniq(combo_3):
                        return []
                    return [merge_lists([pot_14,
                                    get_team_pairs(combo_3)]), combo_3]
                return list(map(check_3combo,
                            combinations(player_tpairs, 17 - get_split())))
            def clean_up_empties(found_list):
                return list(filter(lambda a: a != [], found_list))
            def found_3_vals(val_list):
                def found_3_max(max_val):
                    def found_3_rest(last_3_vals):
                        return [this_one_14, max_val,
                                list(map(lambda a: a[1], last_3_vals))]
                    return found_3_rest(list(filter(
                                lambda a: len(a[0]) == max_val, val_list)))
                return found_3_max(max(list(map(len, list(map(
                            lambda a: a[0], val_list))))))
            return found_3_vals(clean_up_empties(pair_list_14(
                get_team_pairs(this_one_14))))
        def after_14s_set(solutions_14):
            return list(map(look_for_3s, solutions_14))
        if get_pre_picks():
            return after_14s_set(list(map(pick_start, get_pre_picks())))
        return after_14s_set(list(map(pick_start, player_tpairs)))
    return ttf_inner(get_player_tpairs())

if __name__ == "__main__":
    output_json(try_to_find_18())
