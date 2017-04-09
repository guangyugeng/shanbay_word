var log = function() {
  console.log(arguments)
}

$(function() {

    $("#registerForm input").jqBootstrapValidation({
        preventSubmit: true,
        submitError: function($form, event, errors) {
            // additional error messages or events
        },
        submitSuccess: function($form, event) {
            // Prevent spam click and default submit behaviour
            $("#btnSubmit").attr("disabled", true);
            event.preventDefault();

            var username = $("input#username").val();
            var nickname = $("input#nickname").val();
            var email = $("input#email").val();
            var password = $("input#password").val();

            var form = {
                username: username,
                nickname: nickname,
                password: password,
                email: email
            };
            log(form.nickname)
            api.userRegister(form, function(response) {

                var r = response
                if(r.success) {
                    console.log('注册成功', arguments)
                    alert("注册成功")
                    location.href = "http://" + location.host + "/login_view"

                } else {
                    console.log('错误', arguments)
                    log(r.message)
                    alert("注册失败")
                }
            })
        },
        filter: function() {
            return $(this).is(":visible");
        },
    });

    $("a[data-toggle=\"tab\"]").click(function(e) {
        e.preventDefault();
        $(this).tab("show");
    });
});

// When clicking on Full hide fail/success boxes
$('#name').focus(function() {
    $('#success').html('');
});
