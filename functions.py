import pandas as pd
import numpy as np
import os
import gspread as gs
import requests
from plotnine import *
from datetime import date
import streamlit as st
path = str(os.getcwd())
current_date = date.today()
cred = str(path) + '/creds.json'
gc = gs.service_account(filename=cred)
sh1 = gc.open('full_data')
sh2 = gc.open('game_totals')
ws1 = sh1.worksheet('Sheet1')
ws2 = sh2.worksheet('Sheet1')

def prop_trend(player: str, player_id=None):
    props = pd.DataFrame.from_dict(ws1.get_all_records())
    game_totals = pd.DataFrame.from_dict(ws2.get_all_records())

    if player_id is None:
        df = props[props['PLAYER_TXT'] == player].sort_values('DATE')

        if len(df['PLAYER_ID'].unique()) == 1:
            pass
        else:
            raise ValueError(f"""Your player seems to have a common name. 
            See the below options for your player, then grab the corresponding PLAYER_ID and add it to the function.
            {st.dataframe(df[['PLAYER_TXT', 'TEAM_NM', 'PLAYER_ID']].drop_duplicates().reset_index(drop=True))}""")
            return

    elif player_id is not None:
        df = props[(props['PLAYER_TXT'] == player) & (props['PLAYER_ID'] == player_id)].sort_values('DATE')

    else:
        raise ValueError('oops,something else went wrong')

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
        # elif i == len(r.json()['player_props']['core_bet_type_27_points']) & r.json()['player_props']['core_bet_type_27_points'][i]['player_id'] != actnet_player_id:
        #     raise ValueError(f"""Looks like your player doesn't have a prop tonight... yet.""")
        else:
            pass

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