//hide loader
$(document).ready(function () {
    $(window).on("load", function () {
      $(".loader-container").fadeOut("slow");
    });

    $("body").on("click", function(e) {
      if($(e.target).is(".PImg img")) {
        $('.sub-links').fadeToggle()
        // console.log('clicked');
      }else{
        $('.sub-links').fadeOut()
      }
   })
  });


  
