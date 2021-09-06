from .models import Hotel
import pandas as pd
df = pd.read_csv("App\data\hotels.csv")
for idx,h in enumerate(df.values):
    h = Hotel(name=h[1],description=h[2],review=h[3],score=h[4],price=h[5],location=h[8],image='{}.jpg'.format(idx+1),amenities=h[10])
    h.save()