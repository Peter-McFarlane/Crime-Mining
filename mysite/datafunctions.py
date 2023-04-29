import numpy as np
import pandas as pd
pd.set_option('display.float_format', lambda x: '%.3f' % x)

# creates dataframe from textfile and saves it to a parquet
# ! this should only need to be called once !
def create_dataframe():
    print("generating dataframe...")

    f = open("condensed_data.txt", 'r')
    data = f.readlines()
    f.close()

    datalist = []
    datalist_item = []

    for line in data:
        year = int(line[0:4]) #YEAR

        # PERSONAL INFORMATION

        weight = float(line[391:406]) #WGTPERCY
            # implied 5 decimal places from the right
        age = int(line[160:162]) #V3014
        if year < 2003:
            race = int(line[173:175]) #V2040A
        else:
            race = int(line[175:177]) #V2040B
            # 01 white, 02 black, 03 native, 04 asian
            # AFTER 2003:
            # 05 pacific islander, 06 white-black, 07 white-native, 08 white-asian
            # 09 white-pacific islander, 10 black-native, 11 black-asian, 12 black-pacific islander
            # 13 native-asian, 14 asian-pacific islander, 15 white-black-native, 16 white-black-asian
            # 17 white-native-asian, 18 white-asian-hawaiian, 19 two or three, 20 four or five
            # 98 residue, 99 oou
        sex = int(line[165:166]) #V3018
            # 1 male, 2 female, 8 residue, 9 oou
        sexual_orientation = int(line[336:338]) #V3084
        gender_identity = int(line[340:342]) #V3086
        household_income = int(line[53:55]) #V2026
        urbanicity = int(line[46:48]) #V2143
        reported_to_police = int(line[230:231]) #V3048
        did_not_report = int(line[241:242]) #V3054
        
        # SCREEN QUESTIONS

        victimization_type = int(line[433:434]) #VTYPE
            # 1 violent, 2 property, 3 both
        theft_or_attempted = int(line[200:201]) #V3034
        breakin_or_attempted = int(line[204:206]) #V3036
        motor_vehicle_theft = int(line[209:211]) #V3038
        attacked = int(line[214:215]) #V3040
        # attacked_weapon = int(line[218:219]) #V3042
        # attacked_known = int(line[222:223]) #V3044
        unwanted_sex = int(line[226:227]) #V3046
            # 1 yes, 2 no, 3 refused, 8 residue, 9 oou

        datalist_item.append(year)
        datalist_item.append(weight)

        datalist_item.append(age)
        datalist_item.append(race)
        datalist_item.append(sex)
        datalist_item.append(sexual_orientation)
        datalist_item.append(gender_identity)
        datalist_item.append(household_income)
        datalist_item.append(urbanicity)
        datalist_item.append(reported_to_police)
        datalist_item.append(did_not_report)

        datalist_item.append(victimization_type)
        datalist_item.append(victimization_type)
        datalist_item.append(theft_or_attempted)
        datalist_item.append(breakin_or_attempted)
        datalist_item.append(motor_vehicle_theft)
        datalist_item.append(attacked)
        datalist_item.append(unwanted_sex)

        datalist.append(datalist_item)
        datalist_item = []

    df = pd.DataFrame(datalist, columns=['year', 'weight', 'age', 'race', 'sex', 
                                         'sexual orientation', 'gender identity', 
                                         'household income', 'urban, suburban, or rural', 
                                         'reported to police', 'did not report to police', 
                                         'all violent victimizations', 'all property victimizations',
                                         'thefts and attempted thefts','breakins and attempted breakins', 
                                         'motor vehicle thefts', 'attacks and threats', 'unwanted sexual activity'])
    df.info()
    df.to_parquet('data.parquet', index=False)
    print("generated :)")

def create_graph(characteristic, crime, rate_or_number):

    # read dataframe from parquet
    df = pd.read_parquet('data.parquet', engine='fastparquet')
    valstable = []

    # generates the y values for the graph
    def generate_values():
        if (rate_or_number == "rate"):
        
            available_years = []

            ## calculates total weight per year per characteristic
            grouped = df1.groupby(['year'])['weight'].sum()
            totals = grouped.to_list()

            ## filters for victims of the selected crime
            if crime == 'all violent victimizations':
                df2 = df1[(df1[crime] == 1)]
            elif crime == 'all property victimizations':
                df2 = df1[(df1[crime] == 2)]
            else:
                df2 = df1[df1[crime] == 1]
                
            grouped = df2.groupby(['year', crime])['weight'].sum()
            vals = grouped.to_list()

            ## adds victims of both property and violent crimes to the selected crime
            """
            if (crime == "all property victimizations") or (crime == "all violent victimizations"):
                newvals = []
                for i in range(0,len(vals),2):
                    newval = vals[i] + vals[i+1]
                    newvals.append(newval)
                vals = newvals
            """

            ## in case of missing values for some years
            if len(vals) != 30:
                temp = []

                for item in grouped.items():
                    available_years.append(item[0][0])

                i = 0
                for year in range(1992,2022):
                    if year == available_years[i]:
                        temp.append(vals[i])
                        if i < len(vals) - 1:
                            i = i + 1
                    else:
                        temp.append(0)
        
                vals = temp

            ## in case of missing years for some values
            if len(totals) < 30:
                temp = []

                i = 0
                for year in range(1992,2022):
                    if year == available_years[i]:
                        temp.append(totals[i])
                        i = i + 1
                    else:
                        temp.append(0)
                
                totals = temp
            
            ## calculates the rate of victimizations 
            rates = []
            for i in range(0,30):
                if totals[i] == 0:
                    rate = 0
                else:
                    rate = (vals[i] / totals[i]) * 10
                rates.append(rate)

            valstable.append(rates)
        
        if (rate_or_number == "number"):

            ## filters for victims of the selected crime
            df2 = df1[df1[crime] == 1]
            grouped = df2.groupby(['year', crime])['weight'].sum()
            vals = grouped.to_list()

            valstable.append(vals)

    # generates y values for each characteristic

    # filters by all characteristics
    if (characteristic == "all"):
            df1 = df
            generate_values()

    # filters by age bracket
    elif (characteristic == "age"):
        for bracket in range(1,7):
            if (bracket == 1):
                df1 = df[df['age'] < 18]
            elif (bracket == 2):
                df1 = df[(df['age'] >= 18) & (df['age'] < 25)]
            elif (bracket == 3):
                df1 = df[(df['age'] >= 25) & (df['age'] < 35)]
            elif (bracket == 4):
                df1 = df[(df['age'] >= 35) & (df['age'] < 50)]
            elif (bracket == 5):
                df1 = df[(df['age'] >= 50) & (df['age'] < 65)]
            elif (bracket == 6):
                df1 = df[df['age'] >= 65]
            generate_values()

    # filters by race
    elif (characteristic == "race"):
        for race in range(1,6):
            if (race == 1):
                df1 = df[df['race'] == 1]
            elif (race == 2):
                df1 = df[df['race'] == 2]
            elif (race == 3):
                df1 = df[df['race'] == 3]
            elif (race == 4):
                df1 = df[(df['race'] == 4) | (df['race'] == 5)]
            elif (race == 5):
                df1 = df[(df['race'] >= 6) & (df['race'] < 21)]
            generate_values()

    # filters by sex
    elif (characteristic == "sex"):
        for sex in range(1,3):
            df1 = df[df['sex'] == sex]
            generate_values()

    # filters by sexual orientation
    elif (characteristic == "sexual orientation"):
        for orientation in range(1,5):
            df1 = df[df['sexual orientation'] == orientation]
            generate_values()

    # filters by gender identity
    elif (characteristic == "gender identity"):
        for identity in range(1,4):
            df1 = df[df['gender identity'] == identity]
            generate_values()

    # filters by household income bracket
    elif (characteristic == "household income"):
        for bracket in range(1,7):
            if (bracket == 1):
                df1 = df[df['household income'] < 4]
            elif (bracket == 2):
                df1 = df[(df['household income'] >= 4) & (df['household income'] < 8)]
            elif (bracket == 3):
                df1 = df[(df['household income'] >= 8) & (df['household income'] < 11)]
            elif (bracket == 4):
                df1 = df[(df['household income'] >= 11) & (df['household income'] < 13)]
            elif (bracket == 5):
                df1 = df[df['household income'] == 13]
            elif (bracket == 6):
                df1 = df[df['household income'] > 13]
            generate_values()

    # filters by urban, suburban, or rural
    elif (characteristic == "urban, suburban, or rural"):
        for usr in range(1,4):
            df1 = df[df['urban, suburban, or rural'] == usr]
            generate_values()

    # filters by reported to police
    elif (characteristic == "reported to police"):
            df1 = df[df['reported to police'] == 1]
            generate_values()

    # filters by did not report to police
    elif (characteristic == "did not report to police"):
            df1 = df[df['did not report to police'] == 1]
            generate_values()

    return valstable