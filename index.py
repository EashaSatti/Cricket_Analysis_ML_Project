import streamlit as st
import pandas as pd
import plotly.express as px


# Load your dataset
data = pd.read_csv('ODI_Match_info.csv')

# Set page configuration
st.set_page_config(page_title="Cricket Performance Dashboard", page_icon=":cricket_bat_and_ball:", layout="wide")


# Page background styling
page_bg_img = """
<style>
[data-testid='stAppViewContainer']{
background-color: #7176F8;
filter: blur(20);
opacity: 0.9;
color:#fff;
background: rrepeating-linear-gradient(45deg,red,red 5px,blue);
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# Custom CSS to style tabs
st.markdown(
    """
    <style>
    div.st-emotion-cache-jkfxgf.e1nzilvr5 > p {
        background-color: white; 
        font-size: 15px; 
        font-weight: bold;
        padding: 10px;
        border-radius: 10px;
        color: black; 
    }
   div.st-emotion-cache-12h5x7g.e1nzilvr5,p{
   color:black;
   }
   h3{
   color:white;
   }
    </style>
    """, 
    unsafe_allow_html=True
)

# Title and description
st.markdown("<h1 style='text-align: center; color: white;'>🏏 Cricket Performance Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Analyze team performance, player stats, and match outcomes in detail</p>", unsafe_allow_html=True)

# Columns for the layout
col1, col2 = st.columns([2, 1], gap="small")
col1.markdown("""
    <h2 style='color:white; text-align: ; margin-top:20px;'>Welcome to the Ultimate Cricket Showdown!</h2>
    <p style='color:white; text-align: ;'>Cricket is a dynamic blend of technique, strategy, and teamwork. Each match involves analyzing player performances, team strategies, and pitch conditions. Key metrics include runs scored, wickets taken. Batting and bowling averages provide insights into consistency, while factors like toss decisions and venue conditions influence outcomes. By studying match data, such as winning margins by runs or wickets, we can identify trends and areas for improvement. Ultimately, cricket analysis helps teams refine tactics and gain a competitive edge.</p>
""", unsafe_allow_html=True)
col2.image("https://media.istockphoto.com/id/1165345050/photo/male-cricket-batsman-having-just-hit-ball-during-cricket-match.jpg?s=612x612&w=0&k=20&c=wSt3QuuIMZ6YFCX0OCMoHAyuYELm2KLwpXslgivSybE=")

# Tabs for different views
tab1, tab2, tab3, tab4 = st.tabs(["Overall Winner", "Toss Winner", "Winner by Runs", "Winner by Wickets"])

# Tab1: Overall Winner - Code for analyzing match wins
with tab1:    
          # Selecting relevant columns
          df = data[['team1', 'team2', 'winner']]
    
          st.markdown('<h4 style="color:white;">Highest to Lowest Winning Count of countries</h4>', unsafe_allow_html=True)
    
         # Selecting relevant columns
          df = data[['team1', 'team2', 'winner']]
    
         # Counting the number of wins for each team
          win_counts = df['winner'].value_counts()

         # Creating a DataFrame for the chart
          win_counts_df = pd.DataFrame({'team': win_counts.index, 'wins': win_counts.values})

         # Plotting a bar chart with numerical win counts
          fig = px.bar(win_counts_df, x='team', y='wins', title='Total Wins for Each Team')

         # Display the bar chart
          st.plotly_chart(fig)

# Tab2: Toss Winner countries - Code for analyzing match wins
with tab2:
   col1 , col2 = st.columns(2)

with col1:
    st.markdown(
    '<h4 style="color:white;">Toss Winning By every country</h4>',
    unsafe_allow_html=True
      )    
    toss_winner_counts = data['toss_winner'].value_counts().reset_index()
    toss_winner_counts.columns = ['Country', 'Count']
    fig = px.bar(toss_winner_counts, x='Country', y='Count', color='Country', title='Total Tosses Won by Country')
    fig.update_layout(xaxis_title='Country', yaxis_title='Count')
    st.plotly_chart(fig)

with col2:
      st.markdown('<h4 style="color:white;">Toss Winning match winning </h4>',unsafe_allow_html=True)  
   
      team_win_counts = data[data['toss_winner'] == data['winner']]['winner'].value_counts().reset_index()
      team_win_counts.columns = ['Team', 'Wins']
      fig = px.bar(team_win_counts, x='Wins', y='Team', color='Team')
      fig.update_xaxes(categoryorder='total ascending')
      st.plotly_chart(fig)

with tab3:
     st.markdown('<h4 style="color:white;">Filters the dataset to include only those matches where a team won by runs</h4>',unsafe_allow_html=True) 
     # Filter out matches won by runs
     runs_won_df = data[data['win_by_runs'] > 0]

     # Aggregate total runs won by each country
     runs_won_by_country = runs_won_df.groupby('winner')['win_by_runs'].sum().reset_index()

     # Create a bar chart to show the total runs each country won by
     fig = px.bar(runs_won_by_country, x='winner', y='win_by_runs', 
             title='Total Runs by Which Countries Won the Match',
             labels={'winner': 'Country', 'win_by_runs': 'Total Runs Won by'})

     # Display the chart in Streamlit
     st.plotly_chart(fig)


with tab4:
    st.markdown('<h4 style="color:white;">Filters the dataset to include only those matches where a team won by Wickets</h4>',unsafe_allow_html=True) 

    # Filter out matches won by wickets
    wickets_won_df = data[data['win_by_wickets'] > 0]

    # Aggregate total wickets won by each country
    wickets_won_by_country = wickets_won_df.groupby('winner')['win_by_wickets'].sum().reset_index()

    # Create a bar chart to show the total wickets each country won by
    fig = px.bar(wickets_won_by_country, x='winner', y='win_by_wickets', 
                 title='Total Wickets by Which Countries Won the Match',
                 labels={'winner': 'Country', 'win_by_wickets': 'Total Wickets Won by'})
    
    # Display the chart in Streamlit
    st.plotly_chart(fig)


## Creating Side Bar 
# Sidebar for Team Selection
st.sidebar.header("Comparison of Teams")
team1_unique = data['team1'].unique()
team2_unique = data['team2'].unique()
all_teams = list(set(team1_unique) | set(team2_unique))

team_1 = st.sidebar.selectbox('First Team', all_teams, key='team1')
team_2 = st.sidebar.selectbox('Second Team', all_teams, key='team2')

analyze_btn = st.sidebar.button("Analyze", key='analyze_teams')

if analyze_btn:
    # Filter matches between the two selected teams
    team_comparison = data[((data['team1'] == team_1) & (data['team2'] == team_2)) | 
                           ((data['team1'] == team_2) & (data['team2'] == team_1))]

    if team_comparison.empty:
        st.sidebar.warning(f"No matches have occurred between {team_1} and {team_2}.")
    else:
        # Total matches between the two teams
        st.markdown(f"### Total Matches between {team_1} and {team_2}")
        st.write(len(team_comparison))

        # Wins by each team
        team1_wins = team_comparison[team_comparison['winner'] == team_1].shape[0]
        team2_wins = team_comparison[team_comparison['winner'] == team_2].shape[0]

        st.markdown(f"### Match Wins")
        st.write(f"{team_1} won {team1_wins} matches.")
        st.write(f"{team_2} won {team2_wins} matches.")
        
        # Bar chart for wins
        wins_data = pd.DataFrame({team_1: [team1_wins], team_2: [team2_wins]})
        st.bar_chart(wins_data)

        # Run and wickets-based wins
        st.markdown("### Wins by Runs and Wickets")
        
        # Wins by runs
        team1_runs_won = team_comparison[(team_comparison['winner'] == team_1) & (team_comparison['win_by_runs'] > 0)]['win_by_runs'].sum()
        team2_runs_won = team_comparison[(team_comparison['winner'] == team_2) & (team_comparison['win_by_runs'] > 0)]['win_by_runs'].sum()

        # Wins by wickets
        team1_wickets_won = team_comparison[(team_comparison['winner'] == team_1) & (team_comparison['win_by_wickets'] > 0)]['win_by_wickets'].sum()
        team2_wickets_won = team_comparison[(team_comparison['winner'] == team_2) & (team_comparison['win_by_wickets'] > 0)]['win_by_wickets'].sum()

        st.write(f"{team_1} won by a total of {team1_runs_won} runs and {team1_wickets_won} wickets.")
        st.write(f"{team_2} won by a total of {team2_runs_won} runs and {team2_wickets_won} wickets.")

        # Create bar chart for runs and wickets won
        fig = px.bar(x=[team_1, team_2], y=[team1_runs_won, team2_runs_won],
                     labels={'x': 'Teams', 'y': 'Total Runs Won By'},
                     title="Total Runs Won By Teams")
        st.plotly_chart(fig)

        fig = px.bar(x=[team_1, team_2], y=[team1_wickets_won, team2_wickets_won],
                     labels={'x': 'Teams', 'y': 'Total Wickets Won By'},
                     title="Total Wickets Won By Teams")
        st.plotly_chart(fig)

        # Toss decision comparison
        st.markdown(f"### Toss Decision Analysis")
        toss_decision = team_comparison.groupby(['toss_winner', 'toss_decision']).size().reset_index(name='count')
        
        fig = px.pie(toss_decision, values='count', names='toss_decision', title=f'Toss Decision Outcome between {team_1} and {team_2}')
        st.plotly_chart(fig)

        # Winning after choosing to bat or field
        st.markdown(f"### Winning After Toss Decision")
        bat_win = team_comparison[(team_comparison['toss_decision'] == 'bat') & (team_comparison['winner'] == team_comparison['toss_winner'])].shape[0]
        field_win = team_comparison[(team_comparison['toss_decision'] == 'field') & (team_comparison['winner'] == team_comparison['toss_winner'])].shape[0]

        st.write(f"{team_1} and {team_2} won {bat_win} matches after choosing to bat.")
        st.write(f"{team_1} and {team_2} won {field_win} matches after choosing to field.")

        # Venue Analysis
        st.markdown(f"### Venue Analysis")
        venue_counts = team_comparison['venue'].value_counts()
        st.bar_chart(venue_counts)


# Sidebar for Player Performance Analysis
st.sidebar.header("Player Performance Analysis")
players_unique = data['player_of_match'].unique()
selected_player = st.sidebar.selectbox('Select Player', players_unique, key='selected_player')

analyze_btn2 = st.sidebar.button("Analyze", key='analyze_player')

if analyze_btn2:
    player_performance = data[data['player_of_match'] == selected_player]
    
    if player_performance.empty:
        st.sidebar.warning(f"No performance data available for player {selected_player}.")
    else:
        # Unique countries the player's team played against
        opponent_countries = player_performance[['team1', 'team2']].apply(lambda row: [row['team1'], row['team2']], axis=1).explode().unique()
        st.markdown(f"### Matches against Different Countries")
        st.write(f"{selected_player}'s team played against: {', '.join(opponent_countries)}")

        # Total matches won
        total_wins = player_performance[player_performance['winner'] == selected_player].shape[0]
        st.write(f"Total matches won by {selected_player}'s team: {total_wins}")

        # Venue Analysis
        st.markdown(f"### Venue Analysis")
        venue_counts_player = player_performance['venue'].value_counts()
        st.bar_chart(venue_counts_player)