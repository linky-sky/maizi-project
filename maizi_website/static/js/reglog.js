
    // 注册ajax
  $('#regerror').hide()
  $('#formreg').submit(function(){
    var email = $('#id_email').val();
    var password = $('#id_password').val();
    var yanzhengma = $('#id_yanzhengma').val();
    var source_url = $('#id_source_url').val();
    $.ajax({
      'type':"POST",
      'data':{email:email,password:password,yanzhengma:yanzhengma,source_url:source_url},
      'url':{% url 'maizi:do_reg' %},
      'dataType':'html',
      success:function(result,status,xml){
        $('#regerror').show();
        $('#regerror').text(result);
        if (result.match(/http:\/\/.+/) != null){
          $('#regerror').show();
          $('#regerror').text('页面跳转中.......'); 
          $("input[name='email']").val("").focus();
          $("input[name='password']").val("").focus();
          $("input[name='yanzhengma']").val("").focus();
          location.href = window.location.href}
      },
      error:function(){
        $('#regerror').show();
        $('#regerror').text('Error!!!!!!');
      }
    });
    return false;
    // return True;
  });
  //登录ajax
  $('#logerror').hide()
  $('#formlog').submit(function(){
    var username = $('#id_username').val();
    var password = $('#id_password').val();
    var lgsource_url = $('#lg_source_url').val();
    $.ajax({
      'type':"POST",
      'data':{username:username,password:password,lgsource_url:lgsource_url},
      'url':{% url 'maizi:do_login' %},
      'dataType':'html',
      success:function(data,status,xml){
        $('#logerror').show();
        $('#logerror').text(data);
        if (data.match(/http:\/\/.+/) != null){
          $('#logerror').show();
          $('#logerror').text('页面跳转中.......'); 
          $("input[name='username']").val("").focus();
          $("input[name='password']").val("").focus();
          location.href = window.location.href}
      },
      error:function(){
        $('#logerror').show();
        $('#logerror').text('Error!!!!!!');
      }
    });
    return false;
  });
