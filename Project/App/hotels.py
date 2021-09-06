import pandas as pd
import numpy as np
from .models import Hotel


def hotelDataFrame():
    hotels = Hotel.objects.all()
    data = []
    for h in hotels:
        data.append([h.id,h.name,h.description,h.review,h.score,h.price,h.country,h.city,h.location,h.image,h.amenities])

    hotel_df = pd.DataFrame(data,columns=['hotel_id', 'hotel_name', 'description', 'review','score','price','country','city','location','image','amenities'])
    return hotel_df

def get_hotels(hotels_ids,n):
    hotel_df =  hotelDataFrame()
    H = []
    hotels_list = []
    for idx in hotels_ids:
        h = hotel_df.loc[hotel_df['hotel_id']==idx]
        H.append(h)

    for i in range(n):
        hotels_list.append(list(np.array(H)[i,0]))
    return hotels_list




