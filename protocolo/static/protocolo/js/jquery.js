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
        event.preventDefault();
        var form = $("#upl-form");
        var form_data = new FormData(form[0]);
        var href = $(this).attr("data-href");
        const csrf_token = Cookies.get('csrftoken');

        console.log(form_data);
        $.ajax({
            method: 'POST',
            url: href,
            data: form_data,
            mimeType: "multipart/form-data",
            headers: {'X-CSRFToken': csrf_token},
            contentType: false,
            processData: false,
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