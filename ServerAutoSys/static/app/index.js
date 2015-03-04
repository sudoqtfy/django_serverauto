$(function () {                                                                     
   var disk_usage_per,memory_usage_per;
   $.ajax({
          url:"/app/getPercentInfo/",
          async:false,
          success:function(data){
          var jsondata= JSON.parse(data);
          disk_usage_per = jsondata.disk_usage_per;
          memory_usage_per = jsondata.memory_usage_per;
          web_port_status = jsondata.web_port_status;
          redis_port_status = jsondata.redis_port_status;
          count_users = jsondata.count_users;
          count_groups = jsondata.count_groups;

       }
   
    }); 
    $('.orangeCircle').val(disk_usage_per);
    $('.blueCircle').val(memory_usage_per);
    $('.yellowCircle').val(count_users);
    $('.pinkCircle').val(count_groups);
    $('.greenCircle').val(web_port_status);
    $('.lightOrangeCircle').val(redis_port_status);
    $(document).ready(function() {                                                  
        Highcharts.setOptions({                                                     
            global: {                                                               
                useUTC: false                                                       
            }                                                                       
        });                                                                         
        var per=0;
        $.ajax({
               url:"/app/getDiskInfo/",
               async:false,
               success:function(data){
               var jsondata= JSON.parse(data);
               per = jsondata.percent;
            }
    
         }); 
        var total_mem = 0,used_mem = 0;                                                                           
        $.ajax({
               url:"/app/getMemInfo/",
               async:false,
               success:function(data){
               var jsondata= JSON.parse(data);
               total_mem = jsondata.total;
               used_mem = jsondata.used;
            }
    
         }); 
        var st=0,ut=0,it=0;                                                                           
        $.ajax({
               url:"/app/getCpuInfo/",
               async:false,
               success:function(data){
               var jsondata= JSON.parse(data);
               st = jsondata.system_time;
               ut = jsondata.user_time;
               it = jsondata.idle_time;
            }
    
         }); 

        var m1=0,m5=0,m15=0;                                                                           
        $.ajax({
               url:"/app/getLoadAvg/",
               async:false,
               success:function(data){
               var jsondata= JSON.parse(data);
               m1 = jsondata.m1;
               m5 = jsondata.m5;
               m15 = jsondata.m15;
            }
    
         }); 

        var conn_count=0,est_count=0;
        $.ajax({
               url:"/app/getNetInfo/",
               async:false,
               success:function(data){
               var jsondata= JSON.parse(data);
               est = jsondata.established;
               conn_count = jsondata.count;
            }
    
         }); 
        var chart;                                                                  
        $('#memory').highcharts({                                                
            chart: {                                                                
                type: 'area',                                                     
                animation: Highcharts.svg, // don't animate in old IE               
                marginRight: 10,                                                    
                events: {                                                           
                    load: function() {                                              
                                                                                    
                        // set up the updating of the chart each second             
                        var series = this.series[0];                                
                        setInterval(function() {                                    
                            var x = (new Date()).getTime(), // current time         
                                y = Math.random()*100;                                  
                            $.ajax({
                                   url:"/app/getMemInfo/",
                                   async:false,
                                   success:function(data){
                                   var jsondata= JSON.parse(data);
                                   y = jsondata.used;
                            }
                        
                        }); 
                            series.addPoint([x, y], true, true);                    
                        }, 20000);                                                   
                    }                                                               
                }                                                                   
            },                                                                      
            title: {                                                                
                text: 'Memory Usage (Total: '+Math.round(total_mem/1024/1024)+'M)'                                          
            },                                                                      
            xAxis: {                                                                
                type: 'datetime',                                                   
                tickPixelInterval: 200                                              
            },                                                                      
            yAxis: {                                                                
                title: {                                                            
                    text: 'Used Memory(M)'                                                   
                },                                                                  
                plotLines: [{                                                       
                    value: 0,                                                       
                    width: 1,                                                       
                    color: '#808080'                                                
                }]                                                                  
            },                                                                      
            tooltip: {                                                              
                formatter: function() {                                             
                        return '<b>'+ this.series.name +'</b><br/>'+                
                        Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x) +'<br/>'+
                        Highcharts.numberFormat(Math.round(this.y/1024/1024), 2);                         
                }                                                                   
            },                                                                      
            legend: {                                                               
                enabled: true                                                 
            },                                                                      
            exporting: {                                                            
                enabled:  true                                                     
            },                                                                      
            credits: {
                enabled: false 
            },
            series: [{                                                              
                name: 'Used Memory',                                                
                data: (function() {                                                 
                    // generate an array of random data                             
                    var data = [],                                                  
                        time = (new Date()).getTime(),                              
                        i;                                                          
                                                                                    
                    for (i = -5; i <= 0; i++) {                                    
                        data.push({                                                 
                            x: time + i * 1000,                                     
                            y: used_mem                                     
                        });                                                         
                    }                                                               
                    return data;                                                    
                })()                                                                
            }]                                                                      
        });                                                                         

    //avg load
        $('#avgload').highcharts({                                                
            chart: {                                                                
                type: 'area',                                                     
                animation: Highcharts.svg, // don't animate in old IE               
                marginRight: 10,                                                    
                events: {                                                           
                    load: function() {                                              
                                                                                    
                        // set up the updating of the chart each second             
                        var series0 = this.series[0];                                
                        var series1 = this.series[1];                                
                        var series2 = this.series[2];                                
                        setInterval(function() {                                    
                            var x = (new Date()).getTime(), // current time         
                                mm=m1=Math.random(),
                                m5=0,
                                m15=0;                                  
                            $.ajax({
                                   url:"/app/getLoadAvg/",
                                   async:false,
                                   success:function(data){
                                   var jsondata= JSON.parse(data);
                                   m1 = jsondata.m1;
                                   m5 = jsondata.m5;
                                   m15 = jsondata.m15;
                            }
                        
                        }); 
                            series0.addPoint([x, m1], true, true);                    
                            series1.addPoint([x, m5], true, true);                    
                            series2.addPoint([x, m15], true, true);                    
                        }, 20000);                                                   
                    }                                                               
                }                                                                   
            },                                                                      
            title: {                                                                
                text: 'Server LoadAvg'                                            
            },                                                                      
            xAxis: {                                                                
                type: 'datetime',                                                   
                tickPixelInterval: 200                                              
            },                                                                      
            yAxis: {                                                                
                title: {                                                            
                    text: 'LoadAvg'                                                   
                },                                                                  
                plotLines: [{                                                       
                    value: 0,                                                       
                    width: 1,                                                       
                    color: '#808080'                                                
                }]                                                                  
            },                                                                      
            tooltip: {                                                              
                formatter: function() {                                             
                        return '<b>'+ this.series.name +'</b><br/>'+                
                        Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x) +'<br/>'+
                        Highcharts.numberFormat(this.y, 2);                         
                }                                                                   
            },                                                                      
            legend: {                                                               
                enabled: true                                                 
            },                                                                      
            exporting: {                                                            
                enabled:  true                                                     
            },                                                                      
            credits: {
                enabled: false 
            },
            series: [{                                                              
                name: '1st minute loadavg',                                                
                data: (function() {                                                 
                    // generate an array of random data                             
                    var data = [],                                                  
                        time = (new Date()).getTime(),                              
                        i;                                                          
                                                                                    
                    for (i = -5; i <= 0; i++) {                                    
                        data.push({                                                 
                            x: time + i * 1000,                                     
                            y: m1                                     
                        });                                                         
                    }                                                               
                    return data;                                                    
                })()                                                                
            },{                                                              
                name: '5th minute loadavg',                                                
                data: (function() {                                                 
                    // generate an array of random data                             
                    var data = [],                                                  
                        time = (new Date()).getTime(),                              
                        i;                                                          
                                                                                    
                    for (i = -5; i <= 0; i++) {                                    
                        data.push({                                                 
                            x: time + i * 1000,                                     
                            y: m5                                     
                        });                                                         
                    }                                                               
                    return data;                                                    
                })()                                                                
            },{                                                              
                name: '15th minute loadavg',                                                
                data: (function() {                                                 
                    // generate an array of random data                             
                    var data = [],                                                  
                        time = (new Date()).getTime(),                              
                        i;                                                          
                                                                                    
                    for (i = -5; i <= 0; i++) {                                    
                        data.push({                                                 
                            x: time + i * 1000,                                     
                            y: m15                                      
                        });                                                         
                    }                                                               
                    return data;                                                    
                })()                                                                
            }]                                                                      
        });                                                                         
        //cpu info
        $('#cpuinfo').highcharts({                                                
            chart: {                                                                
                type: 'area',                                                     
                animation: Highcharts.svg, // don't animate in old IE               
                marginRight: 10,                                                    
                events: {                                                           
                    load: function() {                                              
                                                                                    
                        // set up the updating of the chart each second             
                        var series0 = this.series[0];                                
                        var series1 = this.series[1];                                
                        var series2 = this.series[2];                                
                        setInterval(function() {                                    
                            var x = (new Date()).getTime(), // current time         
                                st=0,
                                ut=0,
                                it=0;                                  
                            $.ajax({
                                   url:"/app/getCpuInfo/",
                                   async:false,
                                   success:function(data){
                                   var jsondata= JSON.parse(data);
                                   st = jsondata.system_time;
                                   ut = jsondata.user_time;
                                   it = jsondata.idle_time;
                            }
                        
                        }); 
                            series0.addPoint([x, st], true, true);                    
                            series1.addPoint([x, ut], true, true);                    
                            series2.addPoint([x, it], true, true);                    
                        }, 20000);                                                   
                    }                                                               
                }                                                                   
            },                                                                      
            title: {                                                                
                text: 'Server CpuInfo'                                            
            },                                                                      
            xAxis: {                                                                
                type: 'datetime',                                                   
                tickPixelInterval: 200                                              
            },                                                                      
            yAxis: {                                                                
                title: {                                                            
                    text: 'CPU time'                                                   
                },                                                                  
                plotLines: [{                                                       
                    value: 0,                                                       
                    width: 1,                                                       
                    color: '#808080'                                                
                }]                                                                  
            },                                                                      
            tooltip: {                                                              
                formatter: function() {                                             
                        return '<b>'+ this.series.name +'</b><br/>'+                
                        Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x) +'<br/>'+
                        Highcharts.numberFormat(this.y, 2);                         
                }                                                                   
            },                                                                      
            legend: {                                                               
                enabled: true                                                 
            },                                                                      
            exporting: {                                                            
                enabled:  true                                                     
            },                                                                      
            credits: {
                enabled: false 
            },
            series: [{                                                              
                name: 'system time',                                                
                data: (function() {                                                 
                    // generate an array of random data                             
                    var data = [],                                                  
                        time = (new Date()).getTime(),                              
                        i;                                                          
                                                                                    
                    for (i = -5; i <= 0; i++) {                                    
                        data.push({                                                 
                            x: time + i * 1000,                                     
                            y: st                                     
                        });                                                         
                    }                                                               
                    return data;                                                    
                })()                                                                
            },{                                                              
                name: 'user time',                                                
                data: (function() {                                                 
                    // generate an array of random data                             
                    var data = [],                                                  
                        time = (new Date()).getTime(),                              
                        i;                                                          
                                                                                    
                    for (i = -5; i <= 0; i++) {                                    
                        data.push({                                                 
                            x: time + i * 1000,                                     
                            y: ut                                      
                        });                                                         
                    }                                                               
                    return data;                                                    
                })()                                                                
            },{                                                              
                name: 'idle time',                                                
                data: (function() {                                                 
                    // generate an array of random data                             
                    var data = [],                                                  
                        time = (new Date()).getTime(),                              
                        i;                                                          
                                                                                    
                    for (i = -5; i <= 0; i++) {                                    
                        data.push({                                                 
                            x: time + i * 1000,                                     
                            y: it                                      
                        });                                                         
                    }                                                               
                    return data;                                                    
                })()                                                                
            }]                                                                      
        });                                                                         
//diskinfo
    $('#diskinfo').highcharts({
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false
        },
        title: {
            text: 'Disk Usage'
        },
        credits: {
            enabled: false 
        },
        tooltip: {
            pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    enabled: true,
                    color: '#000000',
                    connectorColor: '#000000',
                    formatter: function() {
                        return '<b>'+ this.point.name +'</b>: '+ this.percentage +' %';
                    }
                }
            }
        },
        series: [{
            type: 'pie',
            name: 'Disk Usage',
            data: [
                ['used',   per],
                {
                    name: 'free',
                    y: 12.8,
                    sliced: true,
                    selected: true
                },
            ]
        }]
    });
//network
//   $('#netinfo').highcharts({
//        chart: {
//            type: 'funnel',
//            marginRight: 100
//        },
//        title: {
//            text: 'network Connection',
//            x: -50
//        },
//        plotOptions: {
//            series: {
//                dataLabels: {
//                    enabled: true,
//                    format: '<b>{point.name}</b> ({point.y:,.0f})',
//                    color: 'black',
//                    softConnector: true
//                },
//                neckWidth: '30%',
//                neckHeight: '25%'
//                
//                //-- Other available options
//                // height: pixels or percent
//                // width: pixels or percent
//            }
//        },
//        legend: {
//            enabled: true
//        },
//        credits: {
//            enabled: false 
//        },
//        series: [{
//            name: 'Unique users',
//            data: [
//                ['Connection Count', conn_count],
//                ['ESTABLISHED Count', est_count]
//            ]
//        }]
//    });



    });                                                                             
});                                                                                                 
