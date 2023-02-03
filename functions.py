import pandas as pd
import numpy as np
# import os
import gspread as gs
import requests
from plotnine import *
from datetime import date
import streamlit as st
# path = str(os.getcwd())
# cred = str(path) + '/creds.json'
gc = gs.service_account_from_dict(st.secrets.cred)
sh1 = gc.open('pts_df')
sh2 = gc.open('blk_df')
sh3 = gc.open('ast_df')
sh4 = gc.open('stl_df')
sh5 = gc.open('reb_df')
sh6 = gc.open('fg3_df')
sh7 = gc.open('com_df')
sh8 = gc.open('game_totals')
sh9 = gc.open('todays_df')
ws1 = sh1.worksheet('Sheet1')
ws2 = sh2.worksheet('Sheet1')
ws3 = sh3.worksheet('Sheet1')
ws4 = sh4.worksheet('Sheet1')
ws5 = sh5.worksheet('Sheet1')
ws6 = sh6.worksheet('Sheet1')
ws7 = sh7.worksheet('Sheet1')
ws8 = sh8.worksheet('Sheet1')
ws9 = sh9.worksheet('Sheet1')

def pts_trend(player_id=None):
    current_date = date.today()
    props = pd.DataFrame.from_dict(ws1.get_all_records())
    game_totals = pd.DataFrame.from_dict(ws8.get_all_records())
    df = props[props['PLAYER_ID'] == player_id].sort_values('DATE')

    if len(df) == 0:
        return st.write("Sorry, that guy sucks and you shouldn't even be able to select him. I'm working on that. Pick someone else.")
    else:
        pass

    actnet_player_id = df['ACTNET_PLAYER_ID'].unique()[0]

    # Set headers
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate, br',
               'Accept-Language': 'en-US,en;q=0.5',
               'Connection': 'keep-alive',
               'Host': 'api.actionnetwork.com',
               'Sec-Fetch-Dest': 'document',
               'Sec-Fetch-Mode': 'navigate',
               'Sec-Fetch-Site': 'none',
               'Sec-Fetch-User': '?1',
               'TE': 'trailers',
               'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:107.0) Gecko/20100101 Firefox/107.0'}

    # Get ACTNET_TEAM_ID for player
    team_id = df.sort_values('DATE').iloc[-1]['ACTNET_TEAM_ID']
    game_id = game_totals[(game_totals['DATE'] == str(current_date)) & (game_totals['ACTNET_TEAM_ID'] == team_id)][
        'ACTNET_GAME_ID'].iloc[0]

    # get player prop
    url = 'https://api.actionnetwork.com/web/v1/games/' + str(game_id) + '/props'
    r = requests.get(url, headers=headers)

    for i in range(len(r.json()['player_props']['core_bet_type_27_points'])):

        if r.json()['player_props']['core_bet_type_27_points'][i]['player_id'] == actnet_player_id:
            pts_prop = r.json()['player_props']['core_bet_type_27_points'][i]['odds']['15'][0]['value']
            break
        else:
            pass
    if 'pts_prop' in locals():
        pass
    else:
        return st.write("That player doesn't have a prop yet. Pick a different one.")

    df['PTS'] = df['PTS'].astype({'PTS': 'int32'})
    df['O_U_PROP'] = np.where(df['PTS'] > pts_prop, 'Over', 'Under')

    # total = r.json()['odds'][0]['total']
    name = df['PLAYER_TXT'].unique()
    team = df['TEAM_NM'].unique()
    p = (ggplot(df)
         + geom_col(aes(x='DATE', y='PTS', fill='O_U_PROP'), show_legend=False)
         # + scale_x_continuous(limits=(df['TOTAL'].min()-1 if total > df['TOTAL'].min() else total,
         #                              df['TOTAL'].max() if total < df['TOTAL'].max() else total),
         #                      breaks=np.arange(df['TOTAL'].min()-1,
         #                                       df['TOTAL'].max()+2 if total < df['TOTAL'].max() else total+1,2))
         # + scale_y_continuous(limits=(df['PTS_PROP_DIFF'].min(),df['PTS_PROP_DIFF'].max()), breaks=np.arange(df['PTS_PROP_DIFF'].min(),df['PTS_PROP_DIFF'].max()+2,3))
         + theme(figure_size=(14, 5), axis_text_x=element_text(angle=65), axis_ticks_major_y=element_blank(),
                 axis_text_y=element_blank())
         + scale_fill_manual(values=['#4ed07d', '#c94444'])
         + labs(title=f'{name[0]} - {team[0]} - Current prop {pts_prop}')
         # + geom_vline(xintercept = total, linetype="dotted", color = "darkgreen", size=1.5, alpha=.6)
         + geom_hline(yintercept=pts_prop, linetype="dashed", colour="blue", size=1, alpha=.4)
         + geom_text(aes(x='DATE', y='PTS', label='PTS'), position=position_nudge(y=1), size=12))
    # + annotate("text", x=total+5, y=1.5, label=f"Current total {total}", angle=0, size=10, color="darkgreen", alpha=.7))
    return st.pyplot(ggplot.draw(p))

def blk_trend(player_id=None):
    current_date = date.today()
    props = pd.DataFrame.from_dict(ws2.get_all_records())
    game_totals = pd.DataFrame.from_dict(ws8.get_all_records())
    df = props[props['PLAYER_ID'] == player_id].sort_values('DATE')

    if len(df) == 0:
        return st.write("Sorry, that guy sucks and you shouldn't even be able to select him. I'm working on that. Pick someone else.")
    else:
        pass

    actnet_player_id = df['ACTNET_PLAYER_ID'].unique()[0]

    # Set headers
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate, br',
               'Accept-Language': 'en-US,en;q=0.5',
               'Connection': 'keep-alive',
               'Host': 'api.actionnetwork.com',
               'Sec-Fetch-Dest': 'document',
               'Sec-Fetch-Mode': 'navigate',
               'Sec-Fetch-Site': 'none',
               'Sec-Fetch-User': '?1',
               'TE': 'trailers',
               'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:107.0) Gecko/20100101 Firefox/107.0'}

    # Get ACTNET_TEAM_ID for player
    team_id = df.sort_values('DATE').iloc[-1]['ACTNET_TEAM_ID']
    game_id = game_totals[(game_totals['DATE'] == str(current_date)) & (game_totals['ACTNET_TEAM_ID'] == team_id)][
        'ACTNET_GAME_ID'].iloc[0]

    # get player prop
    url = 'https://api.actionnetwork.com/web/v1/games/' + str(game_id) + '/props'
    r = requests.get(url, headers=headers)

    for i in range(len(r.json()['player_props']['core_bet_type_25_blocks'])):

        if r.json()['player_props']['core_bet_type_25_blocks'][i]['player_id'] == actnet_player_id:
            blk_prop = r.json()['player_props']['core_bet_type_25_blocks'][i]['odds']['15'][0]['value']
            break
        else:
            pass
    if 'blk_prop' in locals():
        pass
    else:
        return st.write("That player doesn't have a prop yet. Pick a different one.")

    df['BLK'] = df['BLK'].astype({'BLK': 'int32'})
    df['O_U_PROP'] = np.where(df['BLK'] > blk_prop, 'Over', 'Under')

    # total = r.json()['odds'][0]['total']
    name = df['PLAYER_TXT'].unique()
    team = df['TEAM_NM'].unique()
    p = (ggplot(df)
         + geom_col(aes(x='DATE', y='BLK', fill='O_U_PROP'), show_legend=False)
         # + scale_x_continuous(limits=(df['TOTAL'].min()-1 if total > df['TOTAL'].min() else total,
         #                              df['TOTAL'].max() if total < df['TOTAL'].max() else total),
         #                      breaks=np.arange(df['TOTAL'].min()-1,
         #                                       df['TOTAL'].max()+2 if total < df['TOTAL'].max() else total+1,2))
         # + scale_y_continuous(limits=(df['PTS_PROP_DIFF'].min(),df['PTS_PROP_DIFF'].max()), breaks=np.arange(df['PTS_PROP_DIFF'].min(),df['PTS_PROP_DIFF'].max()+2,3))
         + theme(figure_size=(14, 5), axis_text_x=element_text(angle=65), axis_ticks_major_y=element_blank(),
                 axis_text_y=element_blank())
         + scale_fill_manual(values=['#4ed07d', '#c94444'])
         + labs(title=f'{name[0]} - {team[0]} - Current prop {blk_prop}')
         # + geom_vline(xintercept = total, linetype="dotted", color = "darkgreen", size=1.5, alpha=.6)
         + geom_hline(yintercept=blk_prop, linetype="dashed", colour="blue", size=1, alpha=.4)
         + geom_text(aes(x='DATE', y='BLK', label='BLK'), position=position_nudge(y=.25), size=12))
    # + annotate("text", x=total+5, y=1.5, label=f"Current total {total}", angle=0, size=10, color="darkgreen", alpha=.7))
    return st.pyplot(ggplot.draw(p))

def ast_trend(player_id=None):
    current_date = date.today()
    props = pd.DataFrame.from_dict(ws3.get_all_records())
    game_totals = pd.DataFrame.from_dict(ws8.get_all_records())
    df = props[props['PLAYER_ID'] == player_id].sort_values('DATE')

    if len(df) == 0:
        return st.write("Sorry, that guy sucks and you shouldn't even be able to select him. I'm working on that. Pick someone else.")
    else:
        pass

    actnet_player_id = df['ACTNET_PLAYER_ID'].unique()[0]

    # Set headers
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate, br',
               'Accept-Language': 'en-US,en;q=0.5',
               'Connection': 'keep-alive',
               'Host': 'api.actionnetwork.com',
               'Sec-Fetch-Dest': 'document',
               'Sec-Fetch-Mode': 'navigate',
               'Sec-Fetch-Site': 'none',
               'Sec-Fetch-User': '?1',
               'TE': 'trailers',
               'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:107.0) Gecko/20100101 Firefox/107.0'}

    # Get ACTNET_TEAM_ID for player
    team_id = df.sort_values('DATE').iloc[-1]['ACTNET_TEAM_ID']
    game_id = game_totals[(game_totals['DATE'] == str(current_date)) & (game_totals['ACTNET_TEAM_ID'] == team_id)][
        'ACTNET_GAME_ID'].iloc[0]

    # get player prop
    url = 'https://api.actionnetwork.com/web/v1/games/' + str(game_id) + '/props'
    r = requests.get(url, headers=headers)

    for i in range(len(r.json()['player_props']['core_bet_type_26_assists'])):

        if r.json()['player_props']['core_bet_type_26_assists'][i]['player_id'] == actnet_player_id:
            ast_prop = r.json()['player_props']['core_bet_type_26_assists'][i]['odds']['15'][0]['value']
            break
        else:
            pass
    if 'ast_prop' in locals():
        pass
    else:
        return st.write("That player doesn't have a prop yet. Pick a different one.")

    df['AST'] = df['AST'].astype({'AST': 'int32'})
    df['O_U_PROP'] = np.where(df['AST'] > ast_prop, 'Over', 'Under')

    # total = r.json()['odds'][0]['total']
    name = df['PLAYER_TXT'].unique()
    team = df['TEAM_NM'].unique()
    p = (ggplot(df)
         + geom_col(aes(x='DATE', y='AST', fill='O_U_PROP'), show_legend=False)
         # + scale_x_continuous(limits=(df['TOTAL'].min()-1 if total > df['TOTAL'].min() else total,
         #                              df['TOTAL'].max() if total < df['TOTAL'].max() else total),
         #                      breaks=np.arange(df['TOTAL'].min()-1,
         #                                       df['TOTAL'].max()+2 if total < df['TOTAL'].max() else total+1,2))
         # + scale_y_continuous(limits=(df['PTS_PROP_DIFF'].min(),df['PTS_PROP_DIFF'].max()), breaks=np.arange(df['PTS_PROP_DIFF'].min(),df['PTS_PROP_DIFF'].max()+2,3))
         + theme(figure_size=(14, 5), axis_text_x=element_text(angle=65), axis_ticks_major_y=element_blank(),
                 axis_text_y=element_blank())
         + scale_fill_manual(values=['#4ed07d', '#c94444'])
         + labs(title=f'{name[0]} - {team[0]} - Current prop {ast_prop}')
         # + geom_vline(xintercept = total, linetype="dotted", color = "darkgreen", size=1.5, alpha=.6)
         + geom_hline(yintercept=ast_prop, linetype="dashed", colour="blue", size=1, alpha=.4)
         + geom_text(aes(x='DATE', y='AST', label='AST'), position=position_nudge(y=.25), size=12))
    # + annotate("text", x=total+5, y=1.5, label=f"Current total {total}", angle=0, size=10, color="darkgreen", alpha=.7))
    return st.pyplot(ggplot.draw(p))

def stl_trend(player_id=None):
    current_date = date.today()
    props = pd.DataFrame.from_dict(ws4.get_all_records())
    game_totals = pd.DataFrame.from_dict(ws8.get_all_records())
    df = props[props['PLAYER_ID'] == player_id].sort_values('DATE')

    if len(df) == 0:
        return st.write("Sorry, that guy sucks and you shouldn't even be able to select him. I'm working on that. Pick someone else.")
    else:
        pass

    actnet_player_id = df['ACTNET_PLAYER_ID'].unique()[0]

    # Set headers
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate, br',
               'Accept-Language': 'en-US,en;q=0.5',
               'Connection': 'keep-alive',
               'Host': 'api.actionnetwork.com',
               'Sec-Fetch-Dest': 'document',
               'Sec-Fetch-Mode': 'navigate',
               'Sec-Fetch-Site': 'none',
               'Sec-Fetch-User': '?1',
               'TE': 'trailers',
               'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:107.0) Gecko/20100101 Firefox/107.0'}

    # Get ACTNET_TEAM_ID for player
    team_id = df.sort_values('DATE').iloc[-1]['ACTNET_TEAM_ID']
    game_id = game_totals[(game_totals['DATE'] == str(current_date)) & (game_totals['ACTNET_TEAM_ID'] == team_id)][
        'ACTNET_GAME_ID'].iloc[0]

    # get player prop
    url = 'https://api.actionnetwork.com/web/v1/games/' + str(game_id) + '/props'
    r = requests.get(url, headers=headers)

    for i in range(len(r.json()['player_props']['core_bet_type_24_steals'])):

        if r.json()['player_props']['core_bet_type_24_steals'][i]['player_id'] == actnet_player_id:
            stl_prop = r.json()['player_props']['core_bet_type_24_steals'][i]['odds']['15'][0]['value']
            break
        else:
            pass
    if 'stl_prop' in locals():
        pass
    else:
        return st.write("That player doesn't have a prop yet. Pick a different one.")

    df['STL'] = df['STL'].astype({'STL': 'int32'})
    df['O_U_PROP'] = np.where(df['STL'] > stl_prop, 'Over', 'Under')

    # total = r.json()['odds'][0]['total']
    name = df['PLAYER_TXT'].unique()
    team = df['TEAM_NM'].unique()
    p = (ggplot(df)
         + geom_col(aes(x='DATE', y='STL', fill='O_U_PROP'), show_legend=False)
         # + scale_x_continuous(limits=(df['TOTAL'].min()-1 if total > df['TOTAL'].min() else total,
         #                              df['TOTAL'].max() if total < df['TOTAL'].max() else total),
         #                      breaks=np.arange(df['TOTAL'].min()-1,
         #                                       df['TOTAL'].max()+2 if total < df['TOTAL'].max() else total+1,2))
         # + scale_y_continuous(limits=(df['PTS_PROP_DIFF'].min(),df['PTS_PROP_DIFF'].max()), breaks=np.arange(df['PTS_PROP_DIFF'].min(),df['PTS_PROP_DIFF'].max()+2,3))
         + theme(figure_size=(14, 5), axis_text_x=element_text(angle=65), axis_ticks_major_y=element_blank(),
                 axis_text_y=element_blank())
         + scale_fill_manual(values=['#4ed07d', '#c94444'])
         + labs(title=f'{name[0]} - {team[0]} - Current prop {stl_prop}')
         # + geom_vline(xintercept = total, linetype="dotted", color = "darkgreen", size=1.5, alpha=.6)
         + geom_hline(yintercept=stl_prop, linetype="dashed", colour="blue", size=1, alpha=.4)
         + geom_text(aes(x='DATE', y='STL', label='STL'), position=position_nudge(y=.25), size=12))
    # + annotate("text", x=total+5, y=1.5, label=f"Current total {total}", angle=0, size=10, color="darkgreen", alpha=.7))
    return st.pyplot(ggplot.draw(p))

def reb_trend(player_id=None):
    current_date = date.today()
    props = pd.DataFrame.from_dict(ws5.get_all_records())
    game_totals = pd.DataFrame.from_dict(ws8.get_all_records())
    df = props[props['PLAYER_ID'] == player_id].sort_values('DATE')

    if len(df) == 0:
        return st.write("Sorry, that guy sucks and you shouldn't even be able to select him. I'm working on that. Pick someone else.")
    else:
        pass

    actnet_player_id = df['ACTNET_PLAYER_ID'].unique()[0]

    # Set headers
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate, br',
               'Accept-Language': 'en-US,en;q=0.5',
               'Connection': 'keep-alive',
               'Host': 'api.actionnetwork.com',
               'Sec-Fetch-Dest': 'document',
               'Sec-Fetch-Mode': 'navigate',
               'Sec-Fetch-Site': 'none',
               'Sec-Fetch-User': '?1',
               'TE': 'trailers',
               'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:107.0) Gecko/20100101 Firefox/107.0'}

    # Get ACTNET_TEAM_ID for player
    team_id = df.sort_values('DATE').iloc[-1]['ACTNET_TEAM_ID']
    game_id = game_totals[(game_totals['DATE'] == str(current_date)) & (game_totals['ACTNET_TEAM_ID'] == team_id)][
        'ACTNET_GAME_ID'].iloc[0]

    # get player prop
    url = 'https://api.actionnetwork.com/web/v1/games/' + str(game_id) + '/props'
    r = requests.get(url, headers=headers)

    for i in range(len(r.json()['player_props']['core_bet_type_23_rebounds'])):

        if r.json()['player_props']['core_bet_type_23_rebounds'][i]['player_id'] == actnet_player_id:
            reb_prop = r.json()['player_props']['core_bet_type_23_rebounds'][i]['odds']['15'][0]['value']
            break
        else:
            pass
    if 'reb_prop' in locals():
        pass
    else:
        return st.write("That player doesn't have a prop yet. Pick a different one.")

    df['REB'] = df['REB'].astype({'REB': 'int32'})
    df['O_U_PROP'] = np.where(df['REB'] > reb_prop, 'Over', 'Under')

    # total = r.json()['odds'][0]['total']
    name = df['PLAYER_TXT'].unique()
    team = df['TEAM_NM'].unique()
    p = (ggplot(df)
         + geom_col(aes(x='DATE', y='REB', fill='O_U_PROP'), show_legend=False)
         # + scale_x_continuous(limits=(df['TOTAL'].min()-1 if total > df['TOTAL'].min() else total,
         #                              df['TOTAL'].max() if total < df['TOTAL'].max() else total),
         #                      breaks=np.arange(df['TOTAL'].min()-1,
         #                                       df['TOTAL'].max()+2 if total < df['TOTAL'].max() else total+1,2))
         # + scale_y_continuous(limits=(df['PTS_PROP_DIFF'].min(),df['PTS_PROP_DIFF'].max()), breaks=np.arange(df['PTS_PROP_DIFF'].min(),df['PTS_PROP_DIFF'].max()+2,3))
         + theme(figure_size=(14, 5), axis_text_x=element_text(angle=65), axis_ticks_major_y=element_blank(),
                 axis_text_y=element_blank())
         + scale_fill_manual(values=['#4ed07d', '#c94444'])
         + labs(title=f'{name[0]} - {team[0]} - Current prop {reb_prop}')
         # + geom_vline(xintercept = total, linetype="dotted", color = "darkgreen", size=1.5, alpha=.6)
         + geom_hline(yintercept=reb_prop, linetype="dashed", colour="blue", size=1, alpha=.4)
         + geom_text(aes(x='DATE', y='REB', label='REB'), position=position_nudge(y=.25), size=12))
    # + annotate("text", x=total+5, y=1.5, label=f"Current total {total}", angle=0, size=10, color="darkgreen", alpha=.7))
    return st.pyplot(ggplot.draw(p))

def fg3_trend(player_id=None):
    current_date = date.today()
    props = pd.DataFrame.from_dict(ws6.get_all_records())
    game_totals = pd.DataFrame.from_dict(ws8.get_all_records())
    df = props[props['PLAYER_ID'] == player_id].sort_values('DATE')

    if len(df) == 0:
        return st.write("Sorry, that guy sucks and you shouldn't even be able to select him. I'm working on that. Pick someone else.")
    else:
        pass

    actnet_player_id = df['ACTNET_PLAYER_ID'].unique()[0]

    # Set headers
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate, br',
               'Accept-Language': 'en-US,en;q=0.5',
               'Connection': 'keep-alive',
               'Host': 'api.actionnetwork.com',
               'Sec-Fetch-Dest': 'document',
               'Sec-Fetch-Mode': 'navigate',
               'Sec-Fetch-Site': 'none',
               'Sec-Fetch-User': '?1',
               'TE': 'trailers',
               'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:107.0) Gecko/20100101 Firefox/107.0'}

    # Get ACTNET_TEAM_ID for player
    team_id = df.sort_values('DATE').iloc[-1]['ACTNET_TEAM_ID']
    game_id = game_totals[(game_totals['DATE'] == str(current_date)) & (game_totals['ACTNET_TEAM_ID'] == team_id)][
        'ACTNET_GAME_ID'].iloc[0]

    # get player prop
    url = 'https://api.actionnetwork.com/web/v1/games/' + str(game_id) + '/props'
    r = requests.get(url, headers=headers)

    for i in range(len(r.json()['player_props']['core_bet_type_21_3fgm'])):

        if r.json()['player_props']['core_bet_type_21_3fgm'][i]['player_id'] == actnet_player_id:
            fg3_prop = r.json()['player_props']['core_bet_type_21_3fgm'][i]['odds']['15'][0]['value']
            break
        else:
            pass
    if 'fg3_prop' in locals():
        pass
    else:
        return st.write("That player doesn't have a prop yet. Pick a different one.")

    df['FG3M'] = df['FG3M'].astype({'FG3M': 'int32'})
    df['O_U_PROP'] = np.where(df['FG3M'] > fg3_prop, 'Over', 'Under')

    # total = r.json()['odds'][0]['total']
    name = df['PLAYER_TXT'].unique()
    team = df['TEAM_NM'].unique()
    p = (ggplot(df)
         + geom_col(aes(x='DATE', y='FG3M', fill='O_U_PROP'), show_legend=False)
         # + scale_x_continuous(limits=(df['TOTAL'].min()-1 if total > df['TOTAL'].min() else total,
         #                              df['TOTAL'].max() if total < df['TOTAL'].max() else total),
         #                      breaks=np.arange(df['TOTAL'].min()-1,
         #                                       df['TOTAL'].max()+2 if total < df['TOTAL'].max() else total+1,2))
         # + scale_y_continuous(limits=(df['PTS_PROP_DIFF'].min(),df['PTS_PROP_DIFF'].max()), breaks=np.arange(df['PTS_PROP_DIFF'].min(),df['PTS_PROP_DIFF'].max()+2,3))
         + theme(figure_size=(14, 5), axis_text_x=element_text(angle=65), axis_ticks_major_y=element_blank(),
                 axis_text_y=element_blank())
         + scale_fill_manual(values=['#4ed07d', '#c94444'])
         + labs(title=f'{name[0]} - {team[0]} - Current prop {fg3_prop}')
         # + geom_vline(xintercept = total, linetype="dotted", color = "darkgreen", size=1.5, alpha=.6)
         + geom_hline(yintercept=fg3_prop, linetype="dashed", colour="blue", size=1, alpha=.4)
         + geom_text(aes(x='DATE', y='FG3M', label='FG3M'), position=position_nudge(y=.25), size=12))
    # + annotate("text", x=total+5, y=1.5, label=f"Current total {total}", angle=0, size=10, color="darkgreen", alpha=.7))
    return st.pyplot(ggplot.draw(p))

def combo_trend(player_id=None):
    current_date = date.today()
    props = pd.DataFrame.from_dict(ws7.get_all_records())
    game_totals = pd.DataFrame.from_dict(ws8.get_all_records())
    df = props[props['PLAYER_ID'] == player_id].sort_values('DATE')

    if len(df) == 0:
        return st.write("Sorry, that guy sucks and you shouldn't even be able to select him. I'm working on that. Pick someone else.")
    else:
        pass

    actnet_player_id = df['ACTNET_PLAYER_ID'].unique()[0]

    # Set headers
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate, br',
               'Accept-Language': 'en-US,en;q=0.5',
               'Connection': 'keep-alive',
               'Host': 'api.actionnetwork.com',
               'Sec-Fetch-Dest': 'document',
               'Sec-Fetch-Mode': 'navigate',
               'Sec-Fetch-Site': 'none',
               'Sec-Fetch-User': '?1',
               'TE': 'trailers',
               'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:107.0) Gecko/20100101 Firefox/107.0'}

    # Get ACTNET_TEAM_ID for player
    team_id = df.sort_values('DATE').iloc[-1]['ACTNET_TEAM_ID']
    game_id = game_totals[(game_totals['DATE'] == str(current_date)) & (game_totals['ACTNET_TEAM_ID'] == team_id)][
        'ACTNET_GAME_ID'].iloc[0]

    # get player prop
    url = 'https://api.actionnetwork.com/web/v1/games/' + str(game_id) + '/props'
    r = requests.get(url, headers=headers)

    for i in range(len(r.json()['player_props']['core_bet_type_85_points_rebounds_assists'])):

        if r.json()['player_props']['core_bet_type_85_points_rebounds_assists'][i]['player_id'] == actnet_player_id:
            com_prop = r.json()['player_props']['core_bet_type_85_points_rebounds_assists'][i]['odds']['15'][0]['value']
            break
        else:
            pass
    if 'com_prop' in locals():
        pass
    else:
        return st.write("That player doesn't have a prop yet. Pick a different one.")

    df['PTS+REB+AST'] = df['PTS+REB+AST'].astype({'PTS+REB+AST': 'int32'})
    df['O_U_PROP'] = np.where(df['PTS+REB+AST'] > com_prop, 'Over', 'Under')

    # total = r.json()['odds'][0]['total']
    name = df['PLAYER_TXT'].unique()
    team = df['TEAM_NM'].unique()
    p = (ggplot(df)
         + geom_col(aes(x='DATE', y='PTS+REB+AST', fill='O_U_PROP'), show_legend=False)
         # + scale_x_continuous(limits=(df['TOTAL'].min()-1 if total > df['TOTAL'].min() else total,
         #                              df['TOTAL'].max() if total < df['TOTAL'].max() else total),
         #                      breaks=np.arange(df['TOTAL'].min()-1,
         #                                       df['TOTAL'].max()+2 if total < df['TOTAL'].max() else total+1,2))
         # + scale_y_continuous(limits=(df['PTS_PROP_DIFF'].min(),df['PTS_PROP_DIFF'].max()), breaks=np.arange(df['PTS_PROP_DIFF'].min(),df['PTS_PROP_DIFF'].max()+2,3))
         + theme(figure_size=(14, 5), axis_text_x=element_text(angle=65), axis_ticks_major_y=element_blank(),
                 axis_text_y=element_blank())
         + scale_fill_manual(values=['#4ed07d', '#c94444'])
         + labs(title=f'{name[0]} - {team[0]} - Current prop {com_prop}')
         # + geom_vline(xintercept = total, linetype="dotted", color = "darkgreen", size=1.5, alpha=.6)
         + geom_hline(yintercept=com_prop, linetype="dashed", colour="blue", size=1, alpha=.4)
         + geom_text(aes(x='DATE', y='PTS+REB+AST', label='PTS+REB+AST'), position=position_nudge(y=.25), size=12))
    # + annotate("text", x=total+5, y=1.5, label=f"Current total {total}", angle=0, size=10, color="darkgreen", alpha=.7))
    return st.pyplot(ggplot.draw(p))

def get_todays_df():
    todays_df = pd.DataFrame.from_dict(ws9.get_all_records())
    return todays_df

def extract_id(df, user_input):
    return df[df['PLAYER_AND_TM'] == user_input]['NBA_PLAYER_ID'].iloc[0]

def plot_pts():
    todays_df = get_todays_df()
    player = st.session_state['player_input']
    player_id = extract_id(todays_df, player)
    return pts_trend(player_id)

def plot_blk():
    todays_df = get_todays_df()
    player = st.session_state['player_input']
    player_id = extract_id(todays_df, player)
    return blk_trend(player_id)

def plot_ast():
    todays_df = get_todays_df()
    player = st.session_state['player_input']
    player_id = extract_id(todays_df, player)
    return ast_trend(player_id)

def plot_stl():
    todays_df = get_todays_df()
    player = st.session_state['player_input']
    player_id = extract_id(todays_df, player)
    return stl_trend(player_id)

def plot_reb():
    todays_df = get_todays_df()
    player = st.session_state['player_input']
    player_id = extract_id(todays_df, player)
    return reb_trend(player_id)

def plot_fg3():
    todays_df = get_todays_df()
    player = st.session_state['player_input']
    player_id = extract_id(todays_df, player)
    return fg3_trend(player_id)

def plot_com():
    todays_df = get_todays_df()
    player = st.session_state['player_input']
    player_id = extract_id(todays_df, player)
    return combo_trend(player_id)