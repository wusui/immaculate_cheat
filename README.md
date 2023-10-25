[//]: # Copyright (C) 2023 Warren  Usui, MIT License

# IMMACULATE CHEATER

October 23, 2023.

A couple of months ago, a discussion on the Facebook group "Because it's Baseball" speculated on what was the mininmun number of players one needed to be able to handle every possible team pairing on the baseball-reference's Immacuate Grid game.  Someone once posted a 19 player solution, that I have not seen recently.  I managed to find several 19 player solutions but did not find one any shorter.

So because of this annoying thing called the rest of my life, I was unable to continue further until this week.  Looking at posts on the internet, it seems like people have reached a hard limit of 19 players.  I have not found a solution that beats this, and a whole bunch of people including harder-core baseball nerds than me believe that this is the limit.  Also, some folks well versed at category theory and discrete combinatorial optimization have stated that they believe that this is the limit also.  I am not going to argue with them because my mathematics is not strong enough.  I only have a Batchelor's degree in math.

But after looking at the problem for a bit, I realized that it would be computationally too time intensive to try every player combination possible, so I guess that these searches were performed using players that played for many major league baseball teams.  So at this point I decided to pivot my search strategy and approach the problem from a new angle.  I no longer am searching for a good solution, I am searching for any 18 player solution.  To do this, I will try some simple solving algorithms up to a certain point where there are a few team pairings left, and then see if I can find any player outside the optimal list of players that can fill in the gaps.

For example, let's say I that out of the list of players who played for eight or more different teams, I find a list of 17 players that handle all possible pairings except for Boston-Seattle, Boston-Miami, Seattle-Miami, and Miami-Philadelphia.  Now if I find any player who played for Boston, Seattle, Miami and Philadelphia, I can add that player and have an 18 player solution.  I have a feeling that this may be a successful strategy because the player that I find that finally solves the problem could be overlooked by the searches that were using a more limited set of players.

Rather than functioning like a traditional README.md document, I am going to treat this file like a running diary of progress that I make toward this goal.

## FIRST CODE CHECKIN

October 24, 2023.

 - get_everybody.py
 - get_player_teams.py
 
 Get_everybody.py reads https://www.baseballreference.com/leaders/leaders_most_franchises.shtml and produces a list of players (named by a portion of the url for their page).  The code handles players since 1950 in addition to players listed separately in the get_others() function.

Get_player_teams.py writes a dict to plyr_info.json that contains lists of teams that players have played for indexed by player-id.  It scrapes the baseball-reference website and so contains code that slows down the requests so that the website does not shut the connection down because it is communicating with a bot.
