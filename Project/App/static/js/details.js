let a = [{day: 'numeric'}, {month: 'short'}, {year: 'numeric'}];
let addPoste =   '';
let updPst = ''; 
function join(t, a, s) {
  function format(m) {
     let f = new Intl.DateTimeFormat('en', m);
     return f.format(t);
  }
  return a.map(format).join(s);
}

function checkImg(check){
    if(check == 0){
      return '<span class="user-img"><img src="/static/img/unknown-user.png" alt=""></span>'
    }else{
      return `<span class="user-img"><img src="${check}" alt=""></span>`
    }
}
function createStars(n){
  stars = ''
  for(let i=0;i<n;i++){
    stars += '<i class="fas fa-star"></i>'
  }
  for(let i=0;i<5-n;i++){
    stars +='<i class="fas fa-star" id="white-stars"></i>'
  }
  return stars
}


$(document).ready(function(){

    $("body").on("click", function(e) {
      if($(e.target).is("#dots")) {
        $('.options').fadeToggle()
      }else{
        $('.options').fadeOut()
      }
   })

    $('.ratingForm').submit(function(e) {
      e.preventDefault()
      $.ajax({
        url : $('.ratingForm').attr('data-url'),
        type: 'POST',
        data: $('.ratingForm').serialize(),
        dataType: "json" ,
        success: function (data) {
          if(data.error){
            $('.error').text(data.error)

          }else if(data.poste){
            let poste = data.poste
            $('.tComment').after(`<div class="user-comment comment${poste[4]}">
            <div class="row1-wrapper">
                <p class="row-1">
                   ${checkImg(poste[5])}
                    <span class="user-name">${poste[0]} ${poste[1]}</span>
                    <span class="user-rating">
                        ${createStars(poste[3])}
                    </span>
                </p>
                <div class="comment-actions">
                <i class="fas fa-ellipsis-h" id='dots'></i>
                <div class="options">
                 <div class="arrow"></div>
                 <label class="update" onclick=showUpdateForm()>modifier</label>
                <label for="deleteInput" class="delete">supprimer</label>
              </div>
            </div>
            </div>
            <p class="row-2">${poste[2]}</p>
            <p class="datePosted"><small>Commentaire envoyé le ${join(new Date(), a, '-')}</small></p>
        </div>
        `).fadeIn(1000)
        addPoste =   $('.add-comment').clone(true);
        $($('.add-comment')[0]).fadeOut(500).remove()
        $('.comments').append(addPoste[0])
        $('.add-comment').fadeOut()
        // console.log(addPoste[0])
        }
      }

    })
      
    })

  //delete comment action
     $('.deleteForm').submit(function(e) {
      e.preventDefault() 
      $.ajax({
        url : $('.deleteForm').attr('data-url'),
        type: 'POST',
        data:  $('.deleteForm').serialize(),
        dataType: "json" ,
        success: function (data) {
          cls = data.class
          $(`.${cls}`).remove()
          $('.comments').append(addPoste[0])
          $('.add-comment').fadeIn()
      }

    })
    })
   
    $('.editForm').submit(function(e) {
      
      e.preventDefault()
      $.ajax({
        url : $('.editForm').attr('data-url'),
        type: 'POST',
        data: $('.editForm').serialize(),
        dataType: "json" ,
        success: function (data) {
          // console.log(data);
          if(data.error){
            $('.error').text(data.error)

          }
        else if(data.poste){
             let poste = data.poste
            updPst = $(`.comment${poste[4]}`).clone(true)
            $(`.comment${poste[4]}`).remove()
            $(updPst).find('.user-rating').html(createStars(poste[3]))
            $(updPst).find('.row-2').text(poste[2])
            $(updPst).find('.datePosted small').text(`Commentaire envoyé le ${join(new Date(), a, '-')}`)
            $('.editing').fadeOut()
            $('.tComment').after($(updPst)).fadeIn(1000)
        }
      }

    })
      
    })
   
})


function hide(){
  $(function(){
    $('.editing').fadeOut()
  })
}

function showUpdateForm(){
  $(function(){ 
    $('.editing').css('display','flex').fadeIn()
  })
}


