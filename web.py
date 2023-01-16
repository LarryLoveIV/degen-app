import streamlit as st
import pandas as pd
import functions as func
import numpy as np
import os
import glob
import requests
from plotnine import *
from datetime import date
path = str(os.getcwd())
current_date = date.today()

st.title('Burholme Degen')
todays_df = func.get_todays_df()

option = st.selectbox('Start typing a player name.', (todays_df['PLAYER_AND_TM']),
                      on_change=func.plot_player, key='player_input')