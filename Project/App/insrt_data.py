from .models import Hotel, Client, Rating
import pandas as pd 

h_df = pd.read_csv('App/data/hotels.csv')
u_df = pd.read_csv('App/data/users.csv')
r_df = pd.read_csv('App/data/rating.csv')

for idx,h in enumerate(h_df.values):
    hotel = Hotel(name=h[1],description=h[2],review=h[3],score=h[4],price=h[5],location=h[8],image=h[9],amenities=h[10])
    hotel.save()

for c in u_df.values:
    client = Client(firstname=c[1],lastname=c[2],email=c[3],birthdate=c[4],gender=c[5],password='test',h_version=c[6])
    client.save()

for r in r_df.values:
    client = Client.objects.get(id=r[0])
    hotel = Hotel.objects.get(id=r[1])
    rating = Rating(client=client,hotel=hotel,rating=r[2])
    rating.save()





