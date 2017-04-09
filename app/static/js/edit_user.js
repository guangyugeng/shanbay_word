var log = function() {
  console.log(arguments)
}

$(function() {

    $("#editUserForm input").jqBootstrapValidation({
        preventSubmit: true,
        submitError: function($form, event, errors) {
            // additional error messages or events
        },
        submitSuccess: function($form, event) {
            // Prevent spam click and default submit behaviour
            $("#btnSubmit").attr("disabled", true);
            event.preventDefault();

            var nickname = $("input#nickname").val();
            var info = $("textarea#info").val();

            var form = {
                nickname: nickname,
                info: info
            };

            api.userEdit(form, function(response) {
                var r = response
                if(r.success) {
                    alert("编辑成功")
                    location.href = "http://" + location.host + "/user/" + r.username
                } else {
                    console.log('错误', arguments)
                    log(r.message)
                    alert("编辑失败")
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
