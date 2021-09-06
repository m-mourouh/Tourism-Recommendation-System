

(function () {
  
  var form = document.querySelector('.needs-validation')
  form.addEventListener('submit', function (event) {
    if (!form.checkValidity()) {
      event.preventDefault()
      event.stopPropagation()
    }
    
    form.classList.add('was-validated')
  }, false)
  
})()



$(document).ready(function(){
  $('.profileForm').on('submit',function(e){
    e.preventDefault()
    if($('#password').val() != $('#confirmpass').val() )
      $('#confirmpass').prop('required',true);
    
    formdata = new FormData(this);	
    console.log(formdata)
    $('.fileInput').on('change',function(){
      var file = this.files[0];
      if (formdata) {
        formdata.append("profile_img", file);
      }
    })
    // console.log($('.profileForm').serialize())
    // console.log(fileInput.files[0])
    $.ajax({
      url : $('.profileForm').attr('data-url'),
      type: 'POST',
      data: formdata, 
      processData: false,
			contentType: false,
      }).done(function(data){
        console.log(data)
        if(data.error){
          $('#m-c').text(data.error)
        }
        if(data.url){
          window.location.href = data.url
          
        }
      })
      
    })
    $('#deleteAcount').click(function(){
        $('#delete').click()
    })
  

  })
  
  const fileInput = document.querySelector('.fileInput')
  const profileImg = document.querySelector('.user-avatar')
  
  fileInput.addEventListener('change',function(e){
    let file = e.target.files[0] 
    let reader = new FileReader() 
  if(file){
      if(file['type'].includes('image')){
      reader.onload = function(){
          let dataURL = this.result
          profileImg.setAttribute('src',dataURL)
      }
      reader.readAsDataURL(file)
      reader.addEventListener('loadend',function(){
          console.log('image loaded');

      })
    }else{
        alert('Please Select an image') 
    }
  }
})


