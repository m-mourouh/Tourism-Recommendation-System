



function isBlank(str) {
    return (!str || /^\s*$/.test(str));
}

//Ajax 
$(document).ready(function(){
    $('.searchForm').on('submit',function(e){
        query = $('.hotelInput').val()
        if(isBlank(query)){
            $('.error').html('Veuillez entrer un hôtel <div class="arrow-down-1"></div>').css({'padding':'2px 8px','background':'rgba(0,0,0,0.5)'}).fadeIn(1000).fadeOut('slow')
        }else{
            $.ajax({
                url : $('.searchForm').attr('data-url'),
                type: 'POST',
            data: $('.searchForm').serialize()
            
        }).done(function(data){
            if(data.hotels){
                let hotels = data
                const gridContainer = $('.grid-container')
                // console.log(hotels);
                gridContainer.html('')
                $.each(hotels,function(idex,elem){
                    // console.log(elem)   
                    $.each(elem,function(idex,elem){
                        
                        card = document.createElement('div')
                        card.setAttribute('class','card')

                        img = document.createElement('img')
                        img.setAttribute('src','/static/img/hotels/' + elem[9])
                        img.setAttribute('alt','hotel')
                        
                        hotelName = document.createElement('h5')
                        hotelName.setAttribute('class','hotel-name')
                        hotelName.append(elem[1])
        
                        hotelCity = document.createElement('p')
                        hotelCity.setAttribute('class','hotel-city')
                        hotelCity.append(`Hôtel à ${elem[7]}`)
    
                        hotelDesc = document.createElement('p')
                        hotelDesc.setAttribute('class','hotel-description')
                        hotelDesc.append(`Hôtel à ${elem[2]}`)
    
                        watchMore = document.createElement('a')
                        watchMore.setAttribute('class','watch-more')
                        watchMore.setAttribute('href',`/details/${elem[0]}/`)
                        watchMore.append("Voir plus")
    
                        hotelPrice = document.createElement('h5')
                        hotelPrice.setAttribute('class','hotel-price')
                        hotelPrice.append(`À partir de ${elem[5]} MAD par nuit`)
    
                        hotelRating = document.createElement('p')
                        hotelRating.setAttribute('class','hotel-rating')
    
                        b = document.createElement('b')
                        span = document.createElement('span')
                        span.append(elem[4])
                        b.appendChild(span)
                        rate = ''
                            if(elem[4] < 5) rate = "Passable" ;
                            if(elem[4] >= 5 && elem[4] < 5.5) rate = "Moyen" 
                            if(elem[4] >= 5.5 && elem[4] < 6) rate = "Bon" 
                            if(elem[4] >= 6 && elem[4] < 7) rate = "Agréable"
                            if(elem[4] >= 7 && elem[4] < 8) rate = "Bien"
                            if(elem[4] >= 8 && elem[4] < 8.5)  rate = "Trés bien"
                            if(elem[4] >= 8.5 && elem[4] < 9)  rate = "Superbe"
                            if(elem[4] >= 9 && elem[4] < 9.5) rate = "Fabuleux"
                            if(elem[4] >= 9.5 && elem[4] < 10)  rate = "Exceptionnel"
                        // console.log('une erreur s\'est produit!')
                        
                        b.append(` ${rate}`)
                        hotelRating.appendChild(b)
                        hotelRating.append(` . ${elem[3]} expériences vécues`)
    
                        card.appendChild(img)
                        card.appendChild(hotelName)
                        card.appendChild(hotelCity)
                        card.appendChild(hotelDesc)
                        card.appendChild(watchMore)
                        card.appendChild(hotelPrice)
                        card.appendChild(hotelRating)
                        gridContainer.append(card)
                        
                    })
                    })
                    cards = document.querySelectorAll('.card')
                    if(cards.length < 4){
                        n = 4 - cards.length
                        for(i=0;i<n;i++){
                            vc = cards[0].cloneNode(true) 
                            vc.setAttribute('class','card hidden')
                            gridContainer.append(vc)
                        }
                        
                   }
                   $('.card').fadeOut(100).fadeIn(200)
            }else if(data.err){
                // console.log(data.err)
                $('.error').html(`${data.err} <div class="arrow-down-2"></div>`).css({'padding':'2px 8px ','background':'rgba(255,0,0,0.5)'}).fadeIn(1000).fadeOut('slow')

            }
            else{
                console.log('ERROR')
            }
            
        })
        }
            
        e.preventDefault()
    })
})
