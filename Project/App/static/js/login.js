const error = document.querySelector('.error')





//Ajax 
$(document).ready(function(){
    $('.loginForm').on('submit',function(e){
        $.ajax({
            url : $('.loginForm').attr('data-url'),
            type: 'POST',
            data: $('.loginForm').serialize()
            
        }).done(function(data){
            if(data.error){
                error.style.padding = '8px'
                $('.error').text(data.error)
            }else if(data.url){
                window.location.href = data.url
            }
            
        })
            
        e.preventDefault()
    })
})
