import pandas as pd

CSV_URL = 'https://raw.githubusercontent.com/mckeet32/TrevorPublic/master/DKSalaries'

#Read in select columns from csv file url location
df = pd.read_csv(CSV_URL,
        header=0,
        usecols=['Position',
          'NameAndID',
          'Salary',
          'Game Info',
        'TeamAbbrev'
        ])

#Drop any records in which ther is no data nameID or game info
df.dropna(subset=['NameAndID'])
df.dropna(subset=['Game Info'])

#Parse the string in NameAndID to create 2 seperate columns for name and ID
df["PlayerID"] = df["NameAndID"].apply(lambda st: st[st.find("(")+1:st.find(")")])
df["PlayerName"] = df["NameAndID"].apply(lambda st: st[st.find(""):st.find(" (")])

#Extract date of the game from the Game Info field using the date pattern in the field
df["GameDate"] = df["Game Info"].str.extract('(../../....)', expand=True)

#Extract time of the game from the Game Info field using the time pattern in the field
df["GameTime"] = df["Game Info"].str.extract('(..:.... ET)', expand=True)

#Determine the players opponent by comparing TeamAbbrev to the substrings of teams in the game info field
df.loc[df.TeamAbbrev == df["Game Info"].apply(lambda st: st[st.find("@")+1:st.find(" ")]), 'Opponent'] = df["Game Info"].apply(lambda st: st[st.find(""):st.find("@")])
df.loc[df.TeamAbbrev == df["Game Info"].apply(lambda st: st[st.find(""):st.find("@")]), 'Opponent'] = df["Game Info"].apply(lambda st: st[st.find(""):st.find("@")])

#Determine if the players team is home or away by comparing TeamAbbrev to the substring determing home and away team in the game info field
df.loc[df.TeamAbbrev == df["Game Info"].apply(lambda st: st[st.find("@")+1:st.find(" ")]), 'HomeAway'] = 'Home'
df.loc[df.TeamAbbrev == df["Game Info"].apply(lambda st: st[st.find(""):st.find("@")]), 'HomeAway'] = 'Away'

#Create 2nd dataframe for output of fields derived from oirignal dataset
df2 = df[['PlayerID','PlayerName','Salary','TeamAbbrev', 'Opponent','GameDate', 'GameTime', 'HomeAway']]

print(df2)
