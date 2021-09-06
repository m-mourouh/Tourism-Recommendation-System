import pandas as pd 
import numpy as np
from math import sqrt
from .hotels import hotelDataFrame
from .models import Rating


#Recommendation basé Filtrage collaboratif (user to user cf)

def createDataset():
    df = pd.DataFrame(list(Rating.objects.all().values()))
    clients_ids = df.client_id.unique()
    user_ratings = []
    for idn in clients_ids:
        u = df.loc[df['client_id']==idn]
        u = u.drop(['id','comment','datePosted'],axis=1)
        user_ratings.append(list(u.values))
    dataset = {}
    for A in user_ratings:
        for l in A:
            dataset.update({l[0]:{}})
        for l in A:
            x = dataset[l[0]].setdefault(l[1],l[2])
    return dataset



def person_corelation(person1,person2,dataset): 
    both_rated = {}
    for item in dataset[person1]:
        if item in dataset[person2]:
            both_rated[item] = 1

    number_of_ratings = len(both_rated)
    if number_of_ratings == 0:
        return 0

    person1_preferences_sum = sum([dataset[person1][item] for item in both_rated])
    person2_preferences_sum = sum([dataset[person2][item] for item in both_rated])

    # Sum up the squares of preferences of each user
    person1_square_preferences_sum = sum([pow(dataset[person1][item], 2) for item in both_rated])
    person2_square_preferences_sum = sum([pow(dataset[person2][item], 2) for item in both_rated])

    # Sum up the product value of both preferences for each item
    product_sum_of_both_users = sum([dataset[person1][item] * dataset[person2][item] for item in both_rated])

    # Calculate the pearson score
    numerator_value = product_sum_of_both_users - (
    person1_preferences_sum * person2_preferences_sum / number_of_ratings)
    denominator_value = sqrt((person1_square_preferences_sum - pow(person1_preferences_sum, 2) / number_of_ratings) * (
    person2_square_preferences_sum - pow(person2_preferences_sum, 2) / number_of_ratings))
    if denominator_value == 0:
        return 0
    else:
        r = numerator_value / denominator_value
        return r



def recommendation(person):
    # Gets recommendations for a person by using a weighted average of every other user's rankings
    totals = {}  #empty dictionary
    simSums = {} # empty dictionary
    dataset = createDataset()
    for other in dataset:
        # don't compare me to myself
        if other == person:
            continue
        sim = person_corelation(person, other,dataset)

        # ignore scores of zero or lower
        if sim <= 0:
            continue
        for item in dataset[other]:
            # only score hotels i haven't seen yet
            if item not in dataset[person]:
                # Similrity * score
                totals.setdefault(item, 0)
                totals[item] += dataset[other][item] * sim
                # sum of similarities
                simSums.setdefault(item, 0)
                simSums[item] += sim
                # Create the normalized list

    rankings = [(total / simSums[item], item) for item, total in totals.items()]
    rankings.sort(reverse=True)
    # returns the recommended items
    recommendataions_list = [(recommend_item,score) for score, recommend_item in rankings]
    return recommendataions_list


def weighted_average(n):
    hotel_df = hotelDataFrame()
    hotel_cleaned_df = hotel_df.drop(columns=['description', 'location', 'image','amenities'])
    v = hotel_cleaned_df['review']
    r = hotel_cleaned_df['score']
    c = hotel_cleaned_df['score'].mean()
    m = hotel_cleaned_df['review'].quantile(0.70)
    #weighted average
    hotel_cleaned_df['weighted_average']=((r*v)+ (c*m))/(v+m)
    hotel_sorted_ranking = hotel_cleaned_df.sort_values('weighted_average',ascending=False)
    #Select the n best hotels to recommend
    hotels_ids_list = list(hotel_sorted_ranking['hotel_id'].head(n)) 
    return hotels_ids_list




	







