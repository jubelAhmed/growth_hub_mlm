
$(window).on("load", function(){

    //Get the context of the Chart canvas element we want to select
    var ctx = $("#column-chart");

    // Chart Options
    var chartOptions = {
        // Elements options apply to all of the options unless overridden in a dataset
        // In this case, we are setting the border of each bar to be 2px wide and green
        elements: {
            rectangle: {
                borderWidth: 2,
                borderColor: 'rgb(0, 255, 0)',
                borderSkipped: 'bottom'
            }
        },
        responsive: true,
        maintainAspectRatio: false,
        responsiveAnimationDuration:500,
        legend: {
            position: 'top',
        },
        scales: {
            xAxes: [{
                display: true,
                gridLines: {
                    color: "#f3f3f3",
                    drawTicks: false,
                },
                scaleLabel: {
                    display: true,
                }
            }],
            yAxes: [{
                display: true,
                gridLines: {
                    color: "#f3f3f3",
                    drawTicks: false,
                },
                scaleLabel: {
                    display: true,
                },
                ticks: {
                    beginAtZero: true
                }
            }]
        },
        title: {
            display: true,
            text: 'Primary & Premium Memeber Monthly Registration'
        }
    };

    // data_list = []
    // url_link = window.location.href+'dashboard/memberchart/'
    // async function getJsonData() { 
    //     await fetch(url_link).then(data=>{return data.json()}).then(result=>{ 
    //         data_list.push(result.primary)
            
    //         return result 
    //     })  
        
    // };


    url_link = window.location.href+'dashboard/memberchart/'

    var month_name = [{'1':"Jan"},{'2':"Feb"},{'3':"March"},{'4':"April"},{'5':"May"},{'6':"Jun"},{'7':"July"},{'8':"Aug"},{'9':"Sep"},{'10':"Oct"},{'11':"Nov"},{'12':"Dec"}]
    
    fetch(url_link).then(data=>{return data.json()}).then(result=>{
        total_data = Object.keys(result.primary).length

        highest_data = null
        console.log(total_data)
        console.log(result)
        if(Object.keys(result.primary).length >= Object.keys(result.premium).length){
            console.log('ffssss')
            highest_data = result.primary
        }else{
            console.log('fff')
            highest_data =  result.premium
            console.log()
            console.log(highest_data)
        }
        console.log(highest_data)
        labelNew = highest_data && Object.keys(highest_data).length > 0 ? highest_data.map(data=>(month_name[data.created_date__month-1][data.created_date__month])+'-'+data.created_date__year) : []


        primary_data = []
        premium_data = []
        for(let i=0;i<Object.keys(highest_data).length;i++){
           p1 = result.primary[i] ? result.primary[i].total_member : 0
           p2 = result.premium[i] ? result.premium[i].total_member : 0

           primary_data.push(p1)
           premium_data.push(p2)
            
        }
       
        console.log(primary_data)
        console.log(premium_data)
        // primary_data.push(20)
        // premium_data.push(20)
        var chartData = {
            labels: labelNew,
            datasets: [{
                label: "Primary",
                data: primary_data,
                backgroundColor: "#16D39A",
                hoverBackgroundColor: "rgba(22,211,154,.9)",
                borderColor: "transparent"
            }, {
                label: "Premium",
                data: premium_data,
                backgroundColor: "#F98E76",
                hoverBackgroundColor: "rgba(249,142,118,.9)",
                borderColor: "transparent"
            }]
        };
    
        var config = {
            type: 'bar',
    
            // Chart Options
            options : chartOptions,
    
            data : chartData
        };
    
        // Create the chart
        var lineChart = new Chart(ctx, config);
       
    }).catch(err=>{
        
    }) 
     

    
   

    
    // Chart Data
   
});