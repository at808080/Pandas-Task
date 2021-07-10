#0: SETUP

import pandas as pd
import numpy as np

#Access the dataset and store it in a Pandas DataFrame Object
input_file = "TestData-20210319\TestData-20210319.csv"
df = pd.read_csv(input_file)
column_names = df.columns

#Table1: Total Minutes by Item, ranked descending on GrandTotal
allitems = df["Item"].unique()
allstates = np.sort(df["State"].unique())

#Structure the desired dataframe
totalminutesbyitem = pd.DataFrame()
totalminutesbyitem['Item'] = allitems
for state in allstates:
    totalminutesbyitem[state] = 0

for item in allitems:
    itemfilter = (df["Item"] == str(item))
    actions_this_item = df[itemfilter]
    newfilter = (totalminutesbyitem["Item"] == str(item))
    for state in allstates:
        statefilter = (df["State"] == str(state))
        actions_this_state = actions_this_item[statefilter]
        mins_ = actions_this_state['TotMins'].sum()
        totalminutesbyitem.loc[newfilter, state] = mins_
    #totalminutesbyitem["Grand Total"] = totalminutesbyitem.loc[newfilter, allstates].sum() 

totalminutesbyitem = totalminutesbyitem.append(totalminutesbyitem.sum(numeric_only=True, axis=0), ignore_index=True)
totalminutesbyitem.loc[totalminutesbyitem["Item"].isna() == True, "Item"] = "Grand Total"
totalminutesbyitem["Grand Total"] = totalminutesbyitem.sum(axis=1)
print(totalminutesbyitem)

#Table2: Nested Totals

allitems = df["Item"].unique()
allstates = df["State"].unique()

itemgroup1filter = (df["ItemGroup"] == "ItemGroup1")
itemgroup1 = df[itemgroup1filter]["Item"].unique()

itemgroup2filter = (df["ItemGroup"] == "ItemGroup2")
itemgroup2 = df[itemgroup2filter]["Item"].unique()


#Structure the desired dataframe
totalminutesbyitemgroup1 = pd.DataFrame()
totalminutesbyitemgroup1['Item'] = itemgroup1
for state in allstates:
    totalminutesbyitemgroup1[state] = 0

for item in itemgroup1:
    itemfilter = (df["Item"] == str(item))
    actions_this_item = df[itemfilter]
    newfilter = (totalminutesbyitemgroup1["Item"] == str(item))
    for state in allstates:
        statefilter = (df["State"] == str(state))
        actions_this_state = actions_this_item[statefilter]
        mins_ = actions_this_state['TotMins'].sum()
        totalminutesbyitemgroup1.loc[newfilter, state] = mins_
    totalminutesbyitemgroup1["Grand Total"] = totalminutesbyitemgroup1.loc[newfilter, allstates].sum() 

totalminutesbyitemgroup1["Grand Total"] = totalminutesbyitemgroup1.sum(axis=1)
print(totalminutesbyitemgroup1)

#Table3: Item 4 trended by week, with summary of listening (% of minutes by state)
dfitem04 = df[df["Item"] == "Item04"]
allweeks = dfitem04["Week"].unique()
allstates = dfitem04["State"].unique()

totalminutesbyweek = pd.DataFrame()
totalminutesbyweek['Week'] = allweeks
for state in allstates:
    totalminutesbyweek[state] = 0

for week in allweeks:
    weekfilter = (df["Week"] == str(week))
    actions_this_week = dfitem04[weekfilter]
    newfilter = (totalminutesbyweek["Week"] == str(week))
    for state in allstates:
        statefilter = (dfitem04["State"] == str(state))
        actions_this_state = actions_this_week[statefilter]
        mins_ = actions_this_state['TotMins'].sum()
        totalminutesbyweek.loc[newfilter, state] = mins_
    totalminutesbyweek["Grand Total"] = totalminutesbyweek.loc[newfilter, allstates].sum() 

totalminutesbyweek["Grand Total"] = totalminutesbyweek.sum(axis=1)

print(totalminutesbyweek)

percentminutesbyweek = pd.DataFrame()
percentminutesbyweek['Week'] = allweeks
for state in allstates:
    percentminutesbyweek[state] = totalminutesbyweek[state] / totalminutesbyweek["Grand Total"]
percentminutesbyweek["Grand Total"] = 1
print(percentminutesbyweek)

#Table4: AvgMins/Psn for Item07 in State4 (AvgMins/Psn = TotMins/TotPeople for each cell)
dfitem07 = df[df["Item"] == "Item07"]
allweeks = dfitem07["Week"].unique()
markets = ["Market03", "Market06", "Market09", "Market14", "Market20"]

avgminsperperson = pd.DataFrame()
avgminsperperson['Week'] = allweeks
for market in markets:
    avgminsperperson[market] = 0
avgminsperperson["Grand Total"] = 0

for week in allweeks:
    weekfilter = (df["Week"] == str(week))
    actions_this_week = dfitem07[weekfilter]
    newfilter = (totalminutesbyweek["Week"] == str(week))
    for market in markets:
        marketfilter = (dfitem07["Market"] == str(market))
        actions_this_market = actions_this_week[marketfilter]
        mins_ = actions_this_market['TotMins'].sum()
        ppl_ = actions_this_market["TotPeople"].sum()
        avgminsperperson.loc[newfilter, market] = mins_/ppl_
    avgminsperperson["Grand Total"] = avgminsperperson.loc[newfilter, markets].sum() 

avgminsperperson["Grand Total"] = avgminsperperson.mean(axis=1)
#NOT SURE WHAT THE "GRAND TOTAL" COLUMN IN THE TARGET SPREADSHEET HAS ACTUALLY CALCULATED... MY MEAN VALUES ARE DIFFERENT




#Table5: Total People Doing Activity by Day of Week and Time
dfmarket09 = df[df["Market"] == "Market09"]
allweeks = dfmarket09["Week"].unique()
alltimes = ["M-F Afternoon", "M-F Morning", "S&S Afternoon", "S&S Morning"]

totalpeoplebytime = pd.DataFrame()
totalpeoplebytime['Week'] = allweeks
for time in alltimes:
    totalpeoplebytime[time] = 0
totalpeoplebytime["Grand Total"] = 0

for week in allweeks:
    weekfilter = (df["Week"] == str(week))
    actions_this_week = dfmarket09[weekfilter]
    newfilter = (totalpeoplebytime["Week"] == str(week))
    for time in alltimes:
        timefilter = (dfmarket09["TimeOfActivity"] == str(time))
        actions_this_time = actions_this_week[timefilter]
        ppl_ = actions_this_time["TotPeople"].sum()
        totalpeoplebytime.loc[newfilter, time] = ppl_

totalpeoplebytime["Grand Total"] = totalpeoplebytime[alltimes].sum(axis=1) 


#NOT SURE WHAT THE "GRAND TOTAL" COLUMN IN THE TARGET SPREADSHEET HAS ACTUALLY CALCULATED... MY MEAN VALUES ARE DIFFERENT



#Table6: Total People Doing Activity by Day of Week (M-F & S-S fields added together)
totalpeoplebydayofweek = totalpeoplebytime

totalpeoplebydayofweek["M-F Afternoon"] += totalpeoplebydayofweek["M-F Morning"]
totalpeoplebydayofweek["S&S Afternoon"] += totalpeoplebydayofweek["S&S Morning"]
totalpeoplebydayofweek.drop(["M-F Morning", "S&S Morning"], axis=1, inplace=True)
#totalpeoplebydayofweek.drop(["M-F Morning"], axis=1, inplace=True)


print(totalpeoplebydayofweek)


#Table7: Rolling Means

totalpeoplebydayofweekrolling = totalpeoplebydayofweek.rolling(4).mean()
totalpeoplebydayofweekrolling = pd.concat([totalpeoplebydayofweek["Week"], totalpeoplebydayofweekrolling], axis=1).dropna()
#totalpeoplebydayofweekrolling = totalpeoplebydayofweekrolling.shift(-3)
#totalpeoplebydayofweekrolling = totalpeoplebydayofweekrolling.dropna()
print(totalpeoplebydayofweekrolling)