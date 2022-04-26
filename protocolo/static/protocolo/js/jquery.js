console.log("Jquery loaded")
$(document).ready(function (){
    $(document).on("click",".btn",function (){
            var id = $(this).attr("id")
            var href = $(this).attr("data-href")
            console.log(id)
       $.ajax({
           method: 'GET',
           url: href,
           success: function (data){
               console.log("Success!")
               $('.container').html(data)
           },
           error: function (){
                   console.log("Error!")
                   alert("Pagina não disponível.")
           }
       })
    });
});