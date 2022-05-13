console.log("jquery.js loaded")
$(document).ready(function () {
    $(document).on("click", ".jq-btn", function () {
        var href = $(this).attr("data-href");
        $.ajax({
            method: 'GET',
            url: href,
            success: function (data) {
                console.log("Success!");
                $('.container').html(data);
            },
            error: function () {
                console.log("Error!");
                alert("Pagina não disponível.");
            }
        })
    });

    $(document).on("click", ".btn-submit", function () {
        event.preventDefault();
        var href = $(this).attr("data-href");
        const csrf_token = Cookies.get('csrftoken');
        var post_data = $("#question-form").serialize();

        $.ajax({
            method: 'POST',
            url: href,
            data: post_data,
            headers: {'X-CSRFToken': csrf_token},
            async: false,
            success: function (data) {
                console.log("Success!")
                $('.container').html(data);
                return false;
            },
            error: function () {
                console.log("Error!");
                alert("Pagina não disponível.");
            }
        })
    });

    $(document).on("click", ".btn-submit-upl", function () {
        //event.preventDefault();
        var href = $(this).attr("data-href");
        const csrf_token = Cookies.get('csrftoken');
        var post_data = $("#upl-form").serialize();
        $.ajax({
            method: 'POST',
            url: href,
            data: post_data,
            processData: false,
            contentType: false,
            mimeType: "multipart/form-data",
            headers: {'X-CSRFToken': csrf_token},
            async: false,
            success: function (data) {
                console.log("Success! UPL-FORM")
                $('.container').html(data);
                return false;
            },
            error: function () {
                console.log("Error!");
                alert("Pagina não disponível.");
            }
        })
    });
});