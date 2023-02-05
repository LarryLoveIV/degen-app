import streamlit as st
import functions as func

todays_df = func.get_todays_df()

st.title('Burholme Degen')
st.write("""
        Real quick: I'm still working on a proper error message
        for when you select a player whose game doesn't have a prop sheet yet.
        So, if the app breaks then you probably picked a player whose game has no props AT ALL. Just refresh
        the page and try again closer to tip off - or pick a different player from a different game.
        """)

st.selectbox('Start typing a player name. Then, click the prop trend you want.', (todays_df['PLAYER_AND_TM']),
                      #on_change=func.plot_player,
                      key='player_input')

col1, col2, col3, col4= st.columns([1,1,1,1])
col5, col6,col7= st.columns([3,2,3])

with col1:
    st.button('Get PTS', on_click=func.plot_pts)
with col2:
    st.button('Get BLK', on_click=func.plot_blk)
with col3:
    st.button('Get AST', on_click=func.plot_ast)
with col4:
    st.button('Get STL', on_click=func.plot_stl)
with col5:
    st.button('Get REB', on_click=func.plot_reb)
with col6:
    st.button('Get FG3M', on_click=func.plot_fg3)
with col7:
    st.button('Get PTS+REB+AST', on_click=func.plot_com)