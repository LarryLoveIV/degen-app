import streamlit as st
import functions as func

st.title('Burholme Degen')
todays_df = func.get_todays_df()

option = st.selectbox('Start typing a player name.', (todays_df['PLAYER_AND_TM']),
                      on_change=func.plot_player, key='player_input')