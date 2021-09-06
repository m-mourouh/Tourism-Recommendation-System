from django import forms
from django.shortcuts import redirect, render
import pandas as pd
import numpy as np
from .recommendation import weighted_average ,recommendation
from .hotels import get_hotels , hotelDataFrame
from .models import Client, Hotel , Rating
from .forms import ClientForm , ProfileForm 
from django.contrib.auth.hashers import make_password , check_password
from .methods import isBlank 
from .sessions import set_session , destroy_session
from django.http import JsonResponse
from django.core import serializers
from django.core.paginator import Paginator , EmptyPage
from django.contrib import messages

# pour la recommendation
def recommend(request):
    client_id = request.session.get('client_id')
    if not client_id:
        return redirect('login-page')
    else:
        client = Client.objects.get(id=client_id)
        L = recommendation(client_id)
        hotels_ids = [tup[0] for tup in L ]
        if hotels_ids:
              hotel_list = get_hotels(hotels_ids,12)
              context = {'hotels':hotel_list,'client_id':client_id,'client':client}
              return render(request,'recommendation.html',context)
        else:
            return redirect('home-page')
def home(request):
    client_id = request.session.get('client_id')
    if client_id:
        client = Client.objects.get(id=client_id)
    n = 20 #20 hotels
    hotels_ids = weighted_average(n) 
    hotels_array = get_hotels(hotels_ids,n)
    #Pour la recherche
    if request.method == 'POST':
        
        q = request.POST.get('query')
        ids = []
        hotels = Hotel.objects.all().values()
        p = Paginator(hotels,100)
        hotel_page = p.page(p.num_pages)
        #pagination
        hotels = hotel_page
        for h in hotels:
            if str(q).lower() in h['name'].lower() or str(q).lower()  in h['description'].lower() or str(q).lower()  in h['amenities'].lower() or str(q).lower()  in h['location'].lower() or str(q).lower()  in str(h['score']).lower():
                ids.append(h['id'])
            

        if len(ids) > 0:
             hotels_array = get_hotels(ids,len(ids))
             data = {'hotels': hotels_array}
             return JsonResponse(data)
        if len(ids) == 0:
            data = {"err":'Hotel introuvable'}
            return JsonResponse(data)
    context = {'hotels': hotels_array,'client_id':client_id}
    if client_id:
        context.update({'client':client})
    return render(request,'home.html',context)



def signup(request):
    client_id = request.session.get('client_id')
    if client_id:
        return redirect('home-page')
    else:
        if request.method == 'POST':
            form = ClientForm(request.POST)
            if form.is_valid():
                client = Client(firstname=form.cleaned_data['firstname'],lastname=form.cleaned_data['lastname'],email=form.cleaned_data['email'],birthdate=form.cleaned_data['birthdate'],gender=form.cleaned_data['gender'],password=make_password(form.cleaned_data['password']),h_version=form.cleaned_data['h_version'])
                client.save()

                data = {'url': 'http://127.0.0.1:8000/login/'}
                print("success")
                return JsonResponse(data)
            else:
                print('invalid')
                data = {'errors': form.errors}
                return JsonResponse(data)
        else:
            form = ClientForm()
    
        return render(request,'signup.html',{'form':form})

def login(request):
    client_id = request.session.get('client_id')
    if client_id:
        return redirect('home-page')
    else:
        error = ''
        if request.method == 'POST':
                email = request.POST.get('email')
                password1 = request.POST.get('password')

                if isBlank(email) and isBlank(password1):
                    error = "Veuillez entrer vos identifiants"
                    data = {'error':error}
                    return JsonResponse(data)
                else:
                        client = Client.objects.filter(email=email).first()
                        if client:
                            password2 = client.password
                            if check_password(password1,password2):
                                set_session(request,'client_id',client.id)
                                # return redirect('home-page')
                                client = Client.objects.get(id=client.id)
                                query = Rating.objects.filter(client=client)
                                if len(query) < 2 :
                                    h_version = client.h_version
                                    hotels = []
                                    if h_version == 1:
                                        hotels = Hotel.objects.filter(price__lt = 400)
                                    if h_version == 2:
                                        hotels = Hotel.objects.filter(price__gte = 400).filter(price__lt = 1000)
                                    if h_version == 3:
                                        hotels = Hotel.objects.filter(price__gte = 1000)

                                    h1 = hotels[np.random.randint(len(hotels))]
                                    h2 = hotels[np.random.randint(len(hotels))]
                                    while h1 == h2:
                                        h2 = hotels[np.random.randint(len(hotels))]
                            
                                    r1 = Rating(client=client,hotel=h1,rating= [5,4][np.random.randint(2)])
                                    r2 = Rating(client=client,hotel=h2,rating= [3,2,1][np.random.randint(3)])
                                    r1.save()
                                    r2.save()
                                data = {'url': 'http://127.0.0.1:8000/profile/'}
                                return JsonResponse(data)
                                # print('Success')
                            else:
                                error = 'mot de passe incorrect'
                                data = {'error':error}
                                return JsonResponse(data)
                        else:
                            error = "email n'existe pas"
                            data = {'error':error}
                            return JsonResponse(data)
            
        return render(request,'login.html')

def logout(request):
    if 'client_id' in request.session:
        destroy_session(request,'client_id')
        # logout(request)
        return redirect('home-page')
    else:
         return redirect('login-page')


def details(request,id):
    client_id = request.session.get('client_id')
    hotel_df = hotelDataFrame()
    hotel_row = hotel_df.loc[hotel_df['hotel_id']==id]
    client = Client.objects.filter(id=client_id).first()
    hotel = Hotel.objects.get(id=id)
    rates = Rating.objects.all()
    #pagination
    p = Paginator(rates,1000)
    rates_page = p.page(p.num_pages)
    score = float(hotel_row['score'])
    stars = round(score * 0.5)
    postes = []
    comments = []
    has_comment = False
    
    for r in rates_page[::-1]:
        if hotel == r.hotel:
            if not isBlank(r.comment):
                if client == r.client:
                    has_comment = True
                comments.append(r)
        
            
   
    if request.method == 'POST':
        #! Pour l'action de suppression de commentaie
        if request.POST.get('delete'):
            deletedComment = request.POST.get('delete')
            Rating.objects.filter(client=client,hotel=hotel).delete()
            has_comment = False
            data = {'class': deletedComment}
            return JsonResponse(data)
         #! Pour l'action d'ajout de commentaie
        if request.POST.get('status'):
            rate = request.POST.get('rate')
            comment = request.POST.get('comment')
            if rate == None:
                rate = 0

            if rate == 0:
                error = "Veuillez donner votre note pour cet hôtel"
                data = {'error':error}
                return JsonResponse(data)

            if isBlank(comment):
                error = "Veuillez entrer votre commentaire"
                data = {'error':error}
                return JsonResponse(data)
            
            else:
                if not has_comment:
                    rating = Rating(client= client,hotel= hotel,rating=rate,comment=comment)
                    rating.save()
                    has_comment = True
                    poste = [client.firstname,client.lastname,comment,rate,client_id]
                    if client.profile_img:
                        poste.append(client.profile_img.url)
                    else:
                        poste.append(0)

                    data = {'poste': poste}
                    return JsonResponse(data)
        #!Pour la modification de poste
        if request.POST.get('edit'):
            rate = request.POST.get('rate')
            comment = request.POST.get('comment')
            if rate == None:
                rate = 0

            if rate == 0:
                error = "Veuillez donner votre note pour cet hôtel"
                data = {'error':error}
                return JsonResponse(data)

            if isBlank(comment):
                error = "Veuillez entrer votre commentaire"
                data = {'error':error}
                return JsonResponse(data)
            
            else:
                if not has_comment:
                    return redirect('details-page')
                else:
                    rating = Rating.objects.get(client= client,hotel=hotel)
                    rating.rating = rate
                    rating.comment = comment
                    rating.save()
                    has_comment = True
                    poste = [client.firstname,client.lastname,comment,rate,client_id]
                    data = {'poste': poste}
                    return JsonResponse(data)
            
 
    context = {
        'hotel' : list(hotel_row.values[0]) ,
        'amenities' : list(hotel_row.values[0])[10].split('|') ,
        'client_id' : client_id ,
        'client' : client,
        'comments': comments,
        'stars': stars,
        'has_comment': has_comment
    }
    
    return render(request,'details.html',context)



def profile(request):
    client_id = request.session.get('client_id')
    if not  client_id:
        return redirect('login-page')
    else:
        client = Client.objects.filter(id=client_id).first()
        if request.method == 'POST':
            if request.POST.get('deleteAcount'):
                Client.objects.filter(id=client_id).delete()
                destroy_session(request,'client_id')
                return redirect('home-page')
            else:
                if request.POST.get('update'):
                    form = ProfileForm(request.POST,request.FILES)
                    if form.is_valid():
                        if request.POST.get('password') and not isBlank(form.cleaned_data['password']):
                            if form.cleaned_data['password'] == form.cleaned_data['confirmpass']:
                                client.password = make_password(form.cleaned_data['password'])
                                print(form.cleaned_data['password'])
                            else:
                                data = {'error':'les deux mots passes ne sont pas identiques'}
                                return JsonResponse(data)
                        client.firstname = form.cleaned_data['firstname']
                        client.lastname = form.cleaned_data['lastname']
                        client.birthdate = form.cleaned_data['birthdate']
                        client.gender = form.cleaned_data['gender']
                        client.h_version = form.cleaned_data['h_version']
                        client.address = form.cleaned_data['address']
                        client.country = form.cleaned_data['country']
                        client.save()
                        if form.cleaned_data['profile_img']:
                            client.profile_img = form.cleaned_data['profile_img']
                            client.save()
                        data = {'url': 'http://127.0.0.1:8000/profile/'}
                        print("success")
                        return JsonResponse(data)
                    else:
                        print('invalid')
                        data = {'errors': form.errors}
                        return JsonResponse(data)
        else:
            form = ProfileForm()
        
    context = {
        'client_id' : client_id ,
        'client' : client,
        }
    
    return render(request,'profile.html',context)