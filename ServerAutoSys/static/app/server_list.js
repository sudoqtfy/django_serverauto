function keyauth(val){
    $('#disprogress').css('display','block');
    $.get("/app/doKeyAuth?id="+val, function(data){
        jsondata = JSON.parse(data);
        var msg = jsondata.msg
        var res = jsondata.res
      if (res == false)
      {
          $('#errorlable').html(msg);
          $('#disprogress').css('display','none');
          $('#alert-error').css('display','block');
          return false;
      }

      else if (res == true)
      {
          $('#successlable').html(msg);
          $('#disprogress').css('display','none');
          $('#alert-success').css('display','block');
          $('#keyauth'+val).replaceWith('<span class="label label-success">Active</span>');
          $('#uniform-inlineCheckbox'+val).remove();
          return true;
      }
      else
      {
          $('#errorlable').html('error');
          $('#disprogress').css('display','none');
          $('#alert-error').css('display','block');
          return false;
          
      }

    });
}
