$(function ()
{   

    $("#progress").ajaxStart(function(){
        $(this).slideToggle("slow");
    }); 

     $("#progress").ajaxStop(function(){
      $(this).fadeOut("fast",function(){
            $("#resinfo").slideToggle("slow");
       });
     });


    $("#batchAddKeyAuth").click(function(){
            $("#resinfo").css('display','none');
            $.post(
                '/app/batchAddKeyAuth/',
                {serverStr:$('#serverStr').val()},
                function(data){
                var jsondata = JSON.parse(data);
                var success = jsondata.success,success_str = '';
                var failed = jsondata.failed,failed_str = '';
                var i = 0,j = 0;
                for (s in success)
                {
                    success_str = success_str + '<p class="text-left text-success">'+success[s]+'</p>';
                    i += 1;
                }

                for (f in failed)
                {
                    $.each(failed[f], function(k,v){
                        failed_str = failed_str + '<p class="text-left text-error">'+k;
                        failed_str = failed_str + ':'+ v + '</p><hr>';
                        j += 1;
                    });
                }
                $('#Success').html(success_str);
                $('#Failed').html(failed_str);
                $('.label-success').html('Success('+i+')');
                $('.label-important').html('Failed('+j+')');

                
            });
    });

}); 


