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
            log('dsds')


            var username = $("input#username").val();
            var nickname = $("input#nickname").val();
            var email = $("input#email").val();
            var password = $("input#password").val();
//            var message = $("textarea#message").val();
//            var firstName = name; // For Success/Failure Message
//            // Check for white space in name for Success/Fail message
//            if (firstName.indexOf(' ') >= 0) {
//                firstName = name.split(' ').slice(0, -1).join(' ');
//            }
            var form = {
                username: username,
                nickname: nickname,
                password: password,
                email: email
            };
            log(form.nickname)
            api.userRegister(form, function(response) {
                // 直接用一个匿名函数当回调函数传给 weiboDelete
                // 这是 js 常用的方式
                var r = response
                if(r.success) {
                    console.log('注册成功', arguments)
                    alert("注册成功")

                    location.href = "http://" + location.host + "/login_view"
//                     slideUp 可以以动画的形式删掉一个元

                } else {
                    console.log('错误', arguments)
                    log(r.message)
                    alert("注册失败")
                }
            })
//            $.ajax({
//                url: "/api/user/register",
////                url:  "././mail/contact_me.php",
//                type: "POST",
//                data: {
//                    name: name,
//                    phone: phone,
//                    email: email,
//                    message: message
//                },
//                cache: false,
//                success: function(status) {
//                    // Enable button & show success message
//                    $("#btnSubmit").attr("disabled", false);
//                    $('#success').html("<div class='alert alert-success'>");
//                    $('#success > .alert-success').html("<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;")
//                        .append("</button>");
//                    $('#success > .alert-success')
//                        .append("<strong>Your message has been sent. </strong>");
//                    $('#success > .alert-success')
//                        .append('</div>');
//                    console.log('222')
//                    //clear all fields
//                    $('#contactForm').trigger("reset");
//
//                },
//                error: function(status) {
//                    // Fail message
//                    $('#success').html("<div class='alert alert-danger'>");
//                    $('#success > .alert-danger').html("<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;")
//                        .append("</button>");
//                    $('#success > .alert-danger').append("<strong>Sorry " + firstName + ", it seems that my mail server is not responding. Please try again later!");
//                    $('#success > .alert-danger').append('</div>');
//                    //clear all fields
//                    $('#contactForm').trigger("reset");
//                },
//            });
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
