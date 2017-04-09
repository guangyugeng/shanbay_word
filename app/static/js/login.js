var log = function() {
  console.log(arguments)
}

$(function() {

    $("#loginForm input").jqBootstrapValidation({
        preventSubmit: true,
        submitError: function($form, event, errors) {
            // additional error messages or events
        },
        submitSuccess: function($form, event) {
            // Prevent spam click and default submit behaviour
            $("#btnSubmit").attr("disabled", true);
            event.preventDefault();
            log('dsds')

            // get values from FORM
            var username = $("input#username").val();
            var password = $("input#password").val();
            var form = {
                username: username,
                password: password
            };
            api.userLogin(form, function(response) {
                var r = response
                if(r.success) {
                    console.log('成功', arguments)
                    location.href = "http://" + location.host + "/index"
                } else {
                    console.log('错误', arguments)
                    alert("登录失败")
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
