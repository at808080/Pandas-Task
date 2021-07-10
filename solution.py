'''
0: SETUP AND INITIALISATION OF GLOBALS
'''

import pandas as pd
import numpy as np

#Access the dataset and store it in a Pandas DataFrame Object
input_file = "TestData-20210319\TestData-20210319.csv"
df = pd.read_csv(input_file)
column_names = df.columns

# round to two decimal places in python pandas
pd.options.display.float_format = '{:.0f}'.format

#GLOBAL FUNCTIONS
def addTotalColumn(dataframe: pd.DataFrame):
    '''
    Adds a "Grand Total" Column to the right side of the Dataframe
    '''
    dataframe["Grand Total"] = dataframe.sum(numeric_only=True, axis=1)
    return dataframe

def addTotalRow(dataframe: pd.DataFrame, columnname: str, per: str, toporbottom: str):
    '''
    Appends a "Grand Total" row to either the top or bottom of the Dataframe
    '''
    totalrow = dataframe.sum(numeric_only=True, axis=0)

    #dftotalrow = pd.DataFrame()
    #dftotalrow[per] = "Grand Total"
    #dftotalrow = dftotalrow.append(totalrow, ignore_index=True)
    #dftotalrow.loc("Grand Total") = totalrow
    
    if toporbottom == "bottom":
        dataframe = dataframe.append(totalrow, ignore_index=True)
    elif toporbottom == "top":
        dataframe.loc[-1] = totalrow 
        dataframe.sort_index(inplace=True)
        
        #dataframe = pd.concat([dftotalrow, dataframe],ignore_index=True)
        
    dataframe.loc[dataframe[per].isna() == True, per] = columnname
    return dataframe  

def addTitleRowAbove(dataframe: pd.DataFrame, columnname: str, per: str, colstonull):
    '''
    Adds a row with only data in the leftmost column being the "name" argument
    '''
    dataframe = addTotalRow(dataframe, columnname, per, "top")
    dataframe.loc[dataframe[per] == columnname, colstonull] = None
    dataframe.loc[dataframe[per] == columnname, per] = columnname
    return dataframe

def addMeanRow(dataframe: pd.DataFrame, columnname: str, per: str, toporbottom: str):
    '''
    Appends a "Grand Total" row to either the top or bottom of the Dataframe
    '''
    totalrow = dataframe.mean(numeric_only=True, axis=0)

    #dftotalrow = pd.DataFrame()
    #dftotalrow[per] = "Grand Total"
    #dftotalrow = dftotalrow.append(totalrow, ignore_index=True)
    #dftotalrow.loc("Grand Total") = totalrow
    
    if toporbottom == "bottom":
        dataframe = dataframe.append(totalrow, ignore_index=True)
    elif toporbottom == "top":
        dataframe.loc[-1] = totalrow 
        dataframe.sort_index(inplace=True)
        
        #dataframe = pd.concat([dftotalrow, dataframe],ignore_index=True)
        
    dataframe.loc[dataframe[per].isna() == True, per] = columnname
    return dataframe  


def getConsolidatedTable(dataframe: pd.DataFrame, counting: str, per: str, perfields, by: str, bycolumns):
    '''
    Returns a dataframe with totals of a specified quantity,
    with subtotals per each of a particular set of fields,
    sorted by each of a particular set of columns
    '''
    result = pd.DataFrame()
    result[per] = perfields
    for bycol_ in bycolumns:
        result[bycol_] = 0

    for perfield in perfields:
        perfilter = (dataframe[per] == str(perfield))
        count_this_perfield = dataframe[perfilter]
        finalperfilter = (result[per] == str(perfield))

        for bycol in bycolumns:
            byfilter = (dataframe[by] == str(bycol))
            count_this_bycol = count_this_perfield[byfilter]
            count = count_this_bycol[counting].sum()
            result.loc[finalperfilter, bycol] = count

    return result


'''
Table1: Total Minutes by Item, ranked descending on GrandTotal
'''

#Parameters 
allitems = df["Item"].unique()
allstates = np.sort(df["State"].unique())

minsperitembystate = getConsolidatedTable(dataframe=df, counting="TotMins", per="Item", perfields=allitems, by="State", bycolumns=allstates)
minsperitembystate = addTotalColumn(minsperitembystate)

#Sort by the grand total
minsperitembystate = minsperitembystate.sort_values("Grand Total", ascending=False)

#Add the Grand Total row
minsperitembystate = addTotalRow(minsperitembystate, "Grand Total", "Item", "bottom")

#Print the final dataframe to the console
print("Table1: Total Minutes by Item, ranked descending on GrandTotal")
print(minsperitembystate)


'''
Table2: Nested Totals
'''

#Parameters
allitems = df["Item"].unique()
allstates = np.sort(df["State"].unique())

itemgroup1filter = (df["ItemGroup"] == "ItemGroup1")
itemgroup1 = np.sort(df[itemgroup1filter]["Item"].unique())

itemgroup2filter = (df["ItemGroup"] == "ItemGroup2")
itemgroup2 = np.sort(df[itemgroup2filter]["Item"].unique())


#Item Group 1
dfitemgroup1 = getConsolidatedTable(dataframe=df, counting="TotMins", per="Item", perfields=itemgroup1, by="State", bycolumns=allstates)
dfitemgroup1 = addTotalColumn(dfitemgroup1)
itemgroup1total = dfitemgroup1.sum(numeric_only=True, axis=0)
dfitemgroup1 = addTotalRow(dfitemgroup1, "ItemGroup1", "Item", "top")
#Item Group 2
dfitemgroup2 = getConsolidatedTable(dataframe=df, counting="TotMins", per="Item", perfields=itemgroup2, by="State", bycolumns=allstates)
dfitemgroup2 = addTotalColumn(dfitemgroup2)
itemgroup2total = dfitemgroup2.sum(numeric_only=True, axis=0)
dfitemgroup2 = addTotalRow(dfitemgroup2, "ItemGroup2", "Item", "top")

#Concatenate the two "sub tables" of the two respective item groups
dfbothitemgroups = pd.concat([dfitemgroup1, dfitemgroup2])

#Add a "Grand Total" row
bothitemgroupstotal = (itemgroup1total + itemgroup2total)
bothitemgroupstotal["Item"] = "Grand Total"
dfbothitemgroups = dfbothitemgroups.append(bothitemgroupstotal, ignore_index=True)
dfbothitemgroups.loc[dfbothitemgroups["Item"].isna() == True, "Item"] = "Grand Total"

#Print the final dataframe to the console
print("Table2: Nested Totals")
print(dfbothitemgroups)

'''
Table3: Item 4 trended by week, with summary of listening (% of minutes by state)
'''
dfitem04 = df[df["Item"] == "Item04"]

#Parameters
allweeks = dfitem04["Week"].unique()
allstates = np.sort(dfitem04["State"].unique())

totalminutesbyweek = getConsolidatedTable(dataframe=dfitem04, counting="TotMins", per="Week", perfields=allweeks, by="State", bycolumns=allstates)
totalminutesbyweek = addTotalColumn(totalminutesbyweek)


#Create the relative dataframe by manipulating values from the totalminutesbyweek table
percentminutesbyweek = pd.DataFrame()
percentminutesbyweek['Week'] = allweeks
for state in allstates:
    percentminutesbyweek[state] = 100 * totalminutesbyweek[state] / totalminutesbyweek["Grand Total"]
percentminutesbyweek["Grand Total"] = 100

#Add the final total rows
meanrow = percentminutesbyweek.mean(numeric_only=True, axis=0)
sumrow = totalminutesbyweek.sum(numeric_only=True, axis=0)
percentminutesbyweek = percentminutesbyweek.append(sumrow, ignore_index=True)
percentminutesbyweek = percentminutesbyweek.append(meanrow, ignore_index=True)
percentminutesbyweek.loc[percentminutesbyweek["Week"].isna() == True, "Week"] = "Total % of Mins By State"

#Use Custom function to add "Title Rows" as shown in the excel file, setting a "Title" in the first column and NaN in the other columns to represent empty space
nullcols = ["Grand Total"]
for state in allstates:
    nullcols.append(state)
totalminutesbyweek = addTitleRowAbove(totalminutesbyweek, "TotMins", "Week", colstonull=nullcols)
percentminutesbyweek = addTitleRowAbove(percentminutesbyweek, "% of Mins By State", "Week", colstonull=nullcols)

#combine the two sub dataframes into one final dataframe
dfcombined = pd.concat([totalminutesbyweek, percentminutesbyweek])

#Print the final dataframe to the console
print("Table3: Item 4 trended by week, with summary of listening (% of minutes by state)")
print(dfcombined)

'''
Table4: AvgMins/Psn for Item07 in State4 (AvgMins/Psn = TotMins/TotPeople for each cell)
'''

#Parameters
dfitem07 = df[(df["Item"] == "Item07" ) & (df["State"] == "State4")]
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
avgminsperperson = addMeanRow(avgminsperperson, "Grand Total", "Week", "bottom")

#NOT SURE WHAT THE "GRAND TOTAL" COLUMN IN THE TARGET SPREADSHEET HAS ACTUALLY CALCULATED... MY MEAN VALUES ARE DIFFERENT

#Print the final dataframe to the console
print("Table4: AvgMins/Psn for Item07 in State4 (AvgMins/Psn = TotMins/TotPeople for each cell)")
print(avgminsperperson)

'''
Table5: Total People Doing Activity by Day of Week and Time
'''

#Parameters
dfmarket09 = df[(df["Market"] == "Market09")] # '''& (df["ItemGroup"] == "ItemGroup2")'''
dfmarket09 = dfmarket09[dfmarket09["ItemGroup"] == "ItemGroup2"]
allweeks = dfmarket09["Week"].unique()
alldaysofweek = ["M-F Afternoon", "M-F Morning", "S&S Afternoon", "S&S Morning"]

totalpeoplebytime = getConsolidatedTable(dataframe=dfmarket09, counting="TotPeople", per="Week", perfields=allweeks, by="TimeOfActivity", bycolumns=alldaysofweek)
totalpeoplebytime = addTotalRow(dataframe=totalpeoplebytime, columnname="Grand Total", per="Week", toporbottom="bottom")
totalpeoplebytime = addTotalColumn(totalpeoplebytime)

#Print the final dataframe to the console
print("Table5: Total People Doing Activity by Day of Week and Time")
print(totalpeoplebytime)

'''
Table6: Total People Doing Activity by Day of Week (M-F & S-S fields added together)
'''

totalpeoplebydayofweek = totalpeoplebytime

#Amalgamate columns from Table5 to form Table6 (instead of building from scratch)
totalpeoplebydayofweek["M-F Afternoon"] += totalpeoplebydayofweek["M-F Morning"]
totalpeoplebydayofweek["S&S Afternoon"] += totalpeoplebydayofweek["S&S Morning"]
totalpeoplebydayofweek.drop(["M-F Morning", "S&S Morning"], axis=1, inplace=True)

#Print the final dataframe to the console
print("Table6: Total People Doing Activity by Day of Week (M-F & S-S fields added together)")
print(totalpeoplebydayofweek)


'''
Table7: Rolling Four Week Average People Doing Activity by Day of Week ("4Wk to 2020W13" is average of 202W10-2020W13)
'''

#Use the rolling function to apply the mean function to each row and its previous 3 rows
totalpeoplebydayofweekrolling = totalpeoplebydayofweek.rolling(4).mean()

#drop the first 3 rows as a 4 week rolling mean cannot be calculated for these rows
totalpeoplebydayofweekrolling = pd.concat([totalpeoplebydayofweek["Week"], totalpeoplebydayofweekrolling], axis=1).dropna()
totalpeoplebydayofweekrolling = totalpeoplebydayofweekrolling.loc[totalpeoplebydayofweekrolling["Week"] != "Grand Total"]

#Print the final dataframe to the console
print("Table7: Rolling Four Week Average People Doing Activity by Day of Week ")
print(totalpeoplebydayofweekrolling)