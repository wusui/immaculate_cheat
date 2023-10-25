# Copyright (C) 2023 Warren Usui, MIT License
"""
Get a list of players who played for 8+ franchises
"""
import requests
from bs4 import BeautifulSoup

def get_html():
    """
    Players who played for 8+ teams
    """
    return 'https://www.baseball-reference.com/leaders/' + \
           'leaders_most_franchises.shtml'

def get_others():
    """
    Old players who played for 8+ current MLB teams
    """
    return ['dahlgba01', 'kuzavbo01', 'phillda01', 'wightbi01']

def get_requests():
    """
    Read a remote html file
    """
    return requests.get(get_html(), timeout=30).content

def get_soup():
    """
    Set up Beautiful Soup parser
    """
    return  BeautifulSoup(get_requests(), 'html.parser')

def get_rows():
    """
    Extract all the rows from the first table
    """
    return get_soup().find('table').find_all('tr')

def check_dates(row):
    """
    Make sure fairly current players are used (get_other finds exceptions)
    """
    if not row.find('td'):
        return False
    if int(row.find_all('td')[1].text.split('-')[0]) < 1950:
        return False
    return True

def get_name(row):
    """
    Extract the html info for a player from the href attribute
    """
    return row.find('td').find('a')['href']

def put_in_shtml_text(extra_pl):
    """
    Add html info around get_other() players
    """
    def pist_inner(p_abbrev):
        return f"/players/{p_abbrev[0]}/{p_abbrev}.shtml"
    return list(map(pist_inner, extra_pl))

def get_everybody():
    """
    Return a list of all players who played for 8 or more MLB teams
    """
    return sorted(list(map(get_name, list(filter(check_dates, get_rows()))))
                  + put_in_shtml_text(get_others()))
