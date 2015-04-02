$().ready(function(){
    $("form").submit(function(event){

        event.preventDefault();


        var $form = $(this),
            user = $form.find("input[name='studentid']").val(),
            pwd = $form.find("input[name='password']").val(),
            oid = $form.find("input[name='openid']").val(),
            url = $form.attr("action");
        
        
        console.log(user,pwd,oid,url);
        var posting = $.post(url,{studentid:user,password:pwd,openid:oid})
                        .done(function(){
                            alert("登陆成功,请返回");
                            window.location.href='/';
                        })
                        .fail(function(){
                            alert("验证失败，请重试");})
         
    });
})



