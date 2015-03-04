$(function (){
   $.ajax({
          url:"/app/graph_list/",
          async:false,
          success:function(data){
          var jsondata= JSON.parse(data);
          $._cityInfo = jsondata
       }
    }); 

    $(document).ready(function(){
        $.initProv("#pro", "#city");
    });
})

 
$.initProv = function(prov, city, defaultProv, defaultCity) {
    var provEl = $(prov);
    var cityEl = $(city);
    var hasDefaultProv = (typeof(defaultCity) != 'undefined');
     
    var provHtml = '';
     
    provHtml += '<option value="-1">please choose...</option>';
    for(var i = 0; i < $._cityInfo.length; i++) {
        provHtml += '<option value="' + i + '"' + ((hasDefaultProv && $._cityInfo[i].n == defaultProv) ? ' selected="selected"' : '') + '>' + $._cityInfo[i].n + '</option>';
    }
    provEl.html(provHtml);
    $.initCities(provEl, cityEl, defaultCity);
    provEl.change(function() {
        $.initCities(provEl, cityEl);
    });


    cityEl.change(function(){
        var checkVal = $(this).find("option:selected").val();
        //ajax request
        $.ajax({
               url:"/app/graph_list/?ip="+checkVal+'&a='+ new Date().getTime(),
               async:true,
               success:function(data){
                   $('#rrdimg').html(data);
            }
         }); 
    });
};
 
$.initCities = function(provEl, cityEl, defaultCity) {
    var hasDefaultCity = (typeof(defaultCity) != 'undefined');
    if(provEl.val() != '' && parseInt(provEl.val()) >= 0) {
        var cities = $._cityInfo[parseInt(provEl.val())].c;
        var cityHtml = '';
         
        cityHtml += '<option value="-1">please choose...</option>';
        for(var i = 0; i < cities.length; i++) {
            arr = cities[i].split('_');
            cityHtml += '<option  value="' + arr[0] + '"' + ((hasDefaultCity && cities[i] == defaultCity) ? ' selected="selected"' : '') + '>' + arr[1]+'('+arr[0]+')' + '</option>';
        }
        cityEl.html(cityHtml);
    } else {
        cityEl.html('<option value="-1">please choose...</option>');
    }
};

