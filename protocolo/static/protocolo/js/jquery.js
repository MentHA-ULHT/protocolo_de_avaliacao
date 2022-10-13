console.log("jquery.js loaded");
$(document).ready(function () {

    section = "dashboard-content"
    history.pushState({section: section}, "", ``);

    window.onpopstate = function (event) {
        showSection(event.state.section);
    }

    function showSection(section) {
        $.ajax({
                method: 'GET',
                url: section,
                success: function (data) {
                    $('.page-content').html(data);
                    if (seconds > 0 || ticking) {
                        seconds = 0;
                        ticking = false;
                    }
                    NProgress.done(true);
                },
                error: function () {
                    console.log("Error!");
                    alert("Pagina não disponível.");
                }
            });
    }

        $(document).on("click", ".jq-btn", function () {
            NProgress.start()
            element = $(this)
            var href = element.attr("data-href").replace('#', '');
            console.log(href)
            var section = ""

            if (href == "dashboard"){
                section = "dashboard-content";
            } else {
                section = href;
            }
            history.pushState({section: section}, "", ``);
            showSection(section)
            if (element.hasClass('nav-link')) {
                $(".nav-link").removeClass("active");
            }
            $(this).addClass('active')

        });

        var seconds = 0;
        var ticking = false;

        function tick() {
            if (ticking) {
                var counter = document.getElementById("clock");
                seconds++;
                counter.innerHTML =
                    "0:" + (seconds < 10 ? "0" : "") + String(seconds);
                if (seconds < 60) {
                    setTimeout(tick, 1000);
                } else {
                    document.getElementById("clock").innerHTML = "1:00";
                }
            }
        }

        $(document).on("click", ".btn-timer", function () {
            ico = $('#timer-ico');
            if (ico.hasClass('fa-pause')) {
                ico.removeClass('fa-pause');
                ico.addClass('fa-play');
            } else {
                ico.addClass('fa-pause');
                ico.removeClass('fa-play');
            }
            ticking = (ticking == true) ? false : true
            tick();
        })


        $(document).on("click", ".delete-same-id", function () {
            id = this.id;
            id = id.replace(/\s/g, '');
            console.log(id)
            var list = document.querySelectorAll('#collapse' + $.trim(id))

            for (i = 0; i < list.length; i++) {
                if (i >= 1) {
                    list[i].remove();
                }
            }
        })

        $(document).on("click", ".toggle", function () {
            console.log("on toggle")
            console.log($(this).id)
            e = $(document).getElementsByClassName($(this).id)
            e.toggle();

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
                    $('.page-content').html(data);
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
                    console.log("Success!")
                    $('.page-content').html(data);
                    return false;
                },
                error: function () {
                    console.log("Error!");
                    alert("Pagina não disponível.");
                }
            })
        });

        $(document).on("click", ".jq-report-btn", function () {
            console.log();
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
    }

)
