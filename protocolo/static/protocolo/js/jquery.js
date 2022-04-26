console.log("jquery.js loaded")
$(document).ready(function (){
    $(document).on("click",".btn",function (){
            var id = $(this).attr("id"); //Não é usado para nada, por agora
            var href = $(this).attr("data-href");
       $.ajax({
           method: 'GET',
           url: href,
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