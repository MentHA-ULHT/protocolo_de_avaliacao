console.log("jquery.js loaded")
$(document).ready(function (){
    $(document).on("click",".btn",function (){
            var id = $(this).attr("id"); //Não é usado para nada, por agora
            var href = $(this).attr("data-href");
            const csrf_token = Cookies.get('csrftoken');
       $.ajax({
           method: 'GET',
           url: href,
           headers:{'X-CSRFToken': csrf_token},
           success: function (data){
               console.log("Success!");
               $('.container').html(data);
           },
           error: function (){
                   console.log("Error!");
                   alert("Pagina não disponível.");
           }
       })
    });
});