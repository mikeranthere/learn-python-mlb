#!/usr/bin/python
import requests
delim = ','

def mlb_download_probables():
    # there is a bug. basically if one of the teams hasn't named a started
    # the first pitcher I find gets designated as the visiting pitcher
    # not much I can really do about that.
    staturl = 'http://www.espn.com/mlb/probables'
    # staturl = 'http://www.espn.com/mlb/probables/_/date/20180329'
    staturl = 'http://www.espn.com/mlb/probables/_/date'
    staturl = 'http://m.espn.com/mlb/probables'
    r = requests.get(staturl)
    entries = []
    game_index = []
    j = -1
    Pitcher1Id = ''
    Pitcher2Id = ''
    VisitingTeam = ''
    HomeTeam = ''
    StartTime = ''
    for line in r.iter_lines():
        j = j + 1
        x = line.decode('latin-1')
        ss = x.find('gameId=')
        if ss > -1:
            proc_games(x)
            break
    return()

def proc_games(x):
    # need to do a test with a future game that doesn't have pitchers all decided
    s1 = x.find('gameId=', 0)
    while s1 > -1:
        i = x.find('>', s1)
        j = x.find(' ', i)
        team_1 = x[i+1:j]
        i = x.find(' ', j+1)
        j = x.find(' ', i+1)
        team_2 = x[i+1:j]
        i = x.find(' ', j)
        j = x.find('<', i+1)
        start = x[i+1:j]
        i = x.find('playerId=', j)
        j = x.find('"', i+1)
        pitcher1_id = x[i+9:j]
        i = x.find('>', j)
        j = x.find('<', i+1)
        pitcher1_name = x[i+1:j]
        
        i = x.find('(', j)
        j = x.find(')', i+1)
        pitcher1_throws = x[i+1:j]

        i = j +1
        j = x.find(',', i+1)
        pitcher1_record = x[i+1:j]
        if len(pitcher1_record) > 10:
            # no record. something went wrong
            pitcher1_record = ''
        
        i = x.find('playerId=', j)
        j = x.find('"', i+1)
        pitcher2_id = x[i+9:j]
        i = x.find('>', j)
        j = x.find('<', i+1)
        pitcher2_name = x[i+1:j]
        i = x.find('(', j)
        j = x.find(')', i+1)
        pitcher2_throws = x[i+1:j]

        i = j +1
        j = x.find(',', i+1)
        pitcher2_record = x[i+1:j]
        if len(pitcher2_record) > 10:
            # no record. something went wrong
            pitcher2_record = ''
        
        x = x[i:]  # just far enough so that we'll find a new gameId
        s1 = 0 # reset the index
        s1 = x.find('gameId=', s1)

        row = (team_1 + delim + team_2 + delim + start + delim +
               pitcher1_id + delim + pitcher1_name + delim +
               pitcher1_throws + delim + pitcher1_record + delim +
               pitcher2_id + delim + pitcher2_name + delim +
               pitcher2_throws + delim + pitcher2_record)
        print(row)

    return()
 












mlb_download_probables()

