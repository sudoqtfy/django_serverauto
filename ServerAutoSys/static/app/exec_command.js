var treegrid;
var checkedCustomer = [];
var TreeDeptData;
$(function ()
{   
    window['g'] = 
    $.ajax({
         url:"/app/getAllServerGroup/",
         async:false,
         success:function(data){
         data= JSON.parse(data);
         TreeDeptData = { Rows :data};
        }
    }); 
    treegrid = $("#maingrid").ligerGrid({
        columns: [
            { display: 'groupname/hostname', name: 'name', width: 300, align: 'center', frozen: true },
        { display: 'IP', name: 'ip', width: 150, type: 'int', align: 'left' },
        { display: 'Remote User', name: 'user', width: 150, type: 'int', align: 'left' },
        { display: 'Remote Port', name: 'port', width: 150, type: 'int', align: 'left' },
        { display: 'groupname', name: 'id', width: 150, type: 'int', align: 'left' },
        { display: 'status', name: 'remark', width: 150, align: 'left' }
        ], width: '100%', pageSizeOptions: [5, 10, 15, 20], height: '80%',
        checkbox:true,title:'Server Group',isScroll:false,usePage:true,
        data: TreeDeptData, alternatingRow: false, tree: { columnName: 'name' }, rownumbers: true
    });


    $("#progress").ajaxStart(function(){
        $(this).slideToggle("slow");
//        $(this).show();
    }); 

     $("#progress").ajaxStop(function(){
      $(this).fadeOut("fast",function(){
            $("#resinfo").slideToggle("slow");
       });
     });


    $("#runcommand").click(function(){
            var rows = treegrid.getCheckedRows();
            var ips = "";
            var hosts = "";
            var commands = getArgs();
            $(rows).each(function ()
            {
                if (this.ip)  ips += this.ip + ";";
                if (this.ip && this.name)  hosts += this.name + ";";
            });
            ips = ips.substring(0,ips.length - 1);
            hosts = hosts.substring(0,hosts.length - 1);
            if ( ips == '' || hosts == '' || commands == false)
            {
                alert('Please input ...');
                return false;
            }
            var module = $('#selectmodule').val();
            $("#resinfo").css('display','none');
            $.post(
                '/app/executeCommand/',
                {ip:ips,hosts:hosts,commands:commands,module:module},
                function(data){
                    var jsondata = $.parseJSON(data);
                    var success = jsondata.success,success_str = '';
                    var warning = jsondata.warning,warning_str = '<p class="text-center text-warning lead">--------------Please add the following hostname to the host file------------------</p>';
                    var failed = jsondata.failed,failed_str = '';
                    var i=0,j=0,k=0;
                    for (s in success)
                    {
                        $.each(success[s],function(k,v){
                            success_str = success_str + '<p class="text-center text-success lead">-------------------------'+k+'-------------------------</p>'
                            success_str = success_str + v + '<hr>' 
                            i+=1
                        });
                    }
                    for (f in failed)
                    {
                        $.each(failed[f],function(k,v){
                            failed_str = failed_str + '<p class="text-center text-error lead">-------------------------------'+k+'---------------------------</p>'
                            failed_str = failed_str + v + '<hr>'
                            j+=1
                        });
                    }
                    for (w in warning)
                    {
                        warning_str = warning_str + '<p class="text-left text-warning lead">'+warning[w]+'</p>'
                            k+=1
                    }
                    $('#Success pre').html(success_str);
                    $('#Failed pre').html(failed_str);
                    $('#Warning').html(warning_str);
                    $('.label-success').html('Success('+i+')');
                    $('.label-important').html('Failed('+j+')');
                    $('.label-warning').html('Warning('+k+')');
                
            });
    });




          $('#selectmodule').change(function(){
                $("#textgroup").empty();
                var module_name = $(this).val();
                if (module_name == 'shell')
                {
                    $("#textgroup").append('&nbsp;&nbsp;&nbsp;<input type="text" id="shell" data-source="[&quot;ifconfig&quot;,&quot;df&quot;,&quot;pwd&quot;,&quot;who&quot;,&quot;uptime&quot;,&quot;vmstat&quot;,&quot;netstat -tunlp&quot;,&quot;netstat&quot;,&quot;]" data-items="4" data-provide="typeahead" id="typeahead" class="span6 typeahead" placeholder="shell commands">&nbsp;&nbsp;&nbsp;');
                }
                else if (module_name == 'yum')
                {
//                    if ($('#yum').length > 0){return false}
                    $("#textgroup").append('&nbsp;&nbsp;&nbsp;<input type="text" id="yum" placeholder="package name" class="span6 typeahead"/>&nbsp;&nbsp;&nbsp;');
                }
                else if (module_name == 'script')
                {
                    $("#textgroup").append('&nbsp;&nbsp;&nbsp;<input type="text" id="script" placeholder="local shell script absolute path" class="span6 typeahead"/>&nbsp;&nbsp;&nbsp;');
                }
                else if (module_name == 'copy')
                {
                    $("#textgroup").append('&nbsp;&nbsp;&nbsp;<input type="text" id="copysrc" placeholder="Local absolute path" class="span3 typeahead"/>&nbsp;&nbsp;<input type="text" id="copydest" placeholder="Remote absolute path" class="span3 typeahead"/>&nbsp;&nbsp;&nbsp;');
                }
                else if (module_name == 'cron')
                {
                    $("#textgroup").append('&nbsp;&nbsp;&nbsp;<input type="text" id="copysrc" placeholder="Local path" />&nbsp;&nbsp;<input type="text" id="copydest" placeholder="Remote absolute path" class="span3 typeahead"/>&nbsp;&nbsp;&nbsp;');
                }
                else if (module_name == 'fetch')
                {
                    $("#textgroup").append('&nbsp;&nbsp;&nbsp;<input type="text" id="copysrc" placeholder="The file on the remote system" class="span3 typeahead"/>&nbsp;&nbsp;<input type="text" id="copydest" placeholder="Local path" class="span3 typeahead"/>&nbsp;&nbsp;&nbsp;');
                }

          });

}); 

function getArgs()
{
    if ($('#selectmodule').length == 0 || $('#selectmodule').val() == '')
    {
        return false;
    }
    var val = $('#selectmodule').val();
    if (val == 'shell')
    {
        if ($('#shell').val() == '')
        {
            return false;
        }
        return $('#shell').val();
    }
    else if (val == 'copy')
    {
        if ($('#copysrc').val() =='' || $('#copydest').val() == '')
        {
            return false;
        }
        return 'src='+$('#copysrc').val()+' dest='+$('#copydest').val();
    }
    else if (val == 'script')
    {
        if ($('#script').val() == '' || $('#script').val() == null)
        {
            return false;
        }
        return $('#script').val();
            
    }
    else if (val == 'yum')
    {
        if ($('#yum').val() == '' || $('#yum').val() == null)
        {
            return false;
        }
        return "name="+$('#yum').val()+"  state=present";
            
    }
    else if (val == 'fetch')
    {
        if ($('#copysrc').val() =='' || $('#copydest').val() == '')
        {
            return false;
        }
        return 'src='+$('#copysrc').val()+' dest='+$('#copydest').val();
        
    }
    else
    {
        return false;
    }
}

//        function f_getChecked()
//        {
//            var rows = treegrid.getCheckedRows();
//            var str = "";
//            $(rows).each(function ()
//            {
//                str += this.ip + ",";
//            });
//            alert('选择的是' + str);
//        }
