import streamlit as st
import pandas as pd
import functions
import numpy as np
import os
import glob
import requests
from plotnine import *
from datetime import date
path = str(os.getcwd())
current_date = date.today()

def plot_player():
    player = st.session_state['player_input']
    return functions.prop_trend(player)

st.title('Burholme Degen')

st.text_input(label="Type first initial with a period, then the last name. If there are multiple matches, we'll suggest a player_id to add",
              placeholder="F.Last", on_change=plot_player, key='player_input')

# props_df = pd.read_csv(max(glob.glob(path + '/data/full_data/*'), key=os.path.getmtime), converters={'GAME_ID': '{:2}'.format})
#
# player_df = props_df[props_df['PLAYER_TXT'] == 'K.Johnson']
#
# dup_player = player_df[['PLAYER_TXT', 'TEAM_NM', 'PLAYER_ID']].drop_duplicates()
#
# st.dataframe(dup_player)