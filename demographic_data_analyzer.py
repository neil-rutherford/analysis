import pandas as pd


def calculate_demographic_data(print_data=True):
    # Read data from file
    df = pd.read_csv('adult.data.csv')

    # How many of each race are represented in this dataset? This should be a Pandas series with race names as the index labels.
    race_count = df['race'].value_counts()

    # What is the average age of men?

    new_df = df[df['sex'] == 'Male']
    average_age_men = new_df['age'].mean().round(1)

    # What is the percentage of people who have a Bachelor's degree?
    new_df = df[df['education'] == 'Bachelors']
    percentage_bachelors = round((new_df.shape[0] / df.shape[0]) * 100, 1)

    # What percentage of people with advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?
    # What percentage of people without advanced education make more than 50K?

    advanced_degree = df[(df['education'] == 'Bachelors') | (df['education'] == 'Masters') | (df['education'] == 'Doctorate')]
    more_than_50k = advanced_degree[(advanced_degree['salary'] == '>50K')]

    no_advanced_degree = df[(df['education'] != 'Bachelors') & (df['education'] != 'Masters') & (df['education'] != 'Doctorate')]
    pleb_more_than_50k = no_advanced_degree[(no_advanced_degree['salary'] == '>50K')]

    # with and without `Bachelors`, `Masters`, or `Doctorate`
    higher_education = round((advanced_degree.shape[0] / df.shape[0]) * 100, 1)
    lower_education = round((no_advanced_degree.shape[0] / df.shape[0]) * 100, 1)

    # percentage with salary >50K
    higher_education_rich = round((more_than_50k.shape[0] / advanced_degree.shape[0]) * 100, 1)
    lower_education_rich = round((pleb_more_than_50k.shape[0] / no_advanced_degree.shape[0]) * 100, 1)

    # What is the minimum number of hours a person works per week (hours-per-week feature)?
    min_work_hours = df['hours-per-week'].min()

    # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
    num_min_workers = len(df[df['hours-per-week'] == min_work_hours])

    rich_percentage = round(len(df[(df['hours-per-week'] == min_work_hours) & (df['salary'] == '>50K')]) / num_min_workers * 100, 1)

    # What country has the highest percentage of people that earn >50K?
    new_df = df.loc[(df['salary'] == '>50K')]["native-country"].value_counts()
    new_df2 = df['native-country'].value_counts()
    richest = (new_df / new_df2).max()

    highest_earning_country = (new_df / new_df2).sort_values(ascending=False).index[0]
    highest_earning_country_percentage = round(100 * richest, 1)

    # Identify the most popular occupation for those who earn >50K in India.
    top_IN_occupation = df[(df['salary'] == '>50K') & (df['native-country'] == 'India')]['occupation'].value_counts().keys()[0]

    if print_data:
        print("Number of each race:\n", race_count) 
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupations in India:", top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage':
        highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }
