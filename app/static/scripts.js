// AJAX API REQUEST
window.onload=function() {
    var myRequest = new XMLHttpRequest();
    myRequest.open('GET', myVar1); //myVar1 is the JSON variable passed in from the scores.html jinja


    myRequest.onload = function() {
        var data = myRequest.responseText; //Get the data as a text

        var ourData = JSON.parse(data); //Parse the data, converting it to JSON

        renderHTML(ourData);
    }

    myRequest.send();
};

// CREATE THE CHARTS
function renderHTML(datum) {
    let yaxis = []; //Leaderboard Array
    let frequency = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] //Frequency Distribution Array
    let leaderslabel = [] //Leaders name array (kept blank for privacy)
    for (i = 0; i < datum.marks.length; i++) {
        leaderslabel.push(" ")
        yaxis.push(datum.marks[i]);
        frequency[Math.floor(datum.marks[i]/10)] += 1;
    }
    yaxis.sort(function(a, b){return b - a}); //Sort the array descending (highest scores first)
    

    const CHART = document.getElementById("barGraph"); //Bar Graph of Frequency Distrubution
    const CHART2 = document.getElementById("leaderboard"); //Horizontal Bar Graph of Leaderboard

    let barGraph = new Chart(CHART, {
        type: 'bar',
        data: {
            labels: [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
            datasets: [{
                label: 'Frequency Distribution of Marks',
                data: frequency,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)',
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)',
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)'
                ],
                borderWidth: 1
            },]
        },
        options: {
                    scales: 
                    {
                    xAxes: 
                        [   
                            {
                                display: false,
                                barPercentage: 1.3,
                                ticks: { max: 90,} //Make the Bar graph a Histogram
                            }, 
                            {
                                display: true,
                                ticks: {autoSkip: false,max: 100,}, //Make the Bar graph a Histogram
                                scaleLabel: {display: true, labelString: 'Score (%)'}
                            }
                        ],
                    yAxes: 
                        [
                            {
                                ticks: {beginAtZero:true, precision:0   }, //precision 0 removes decimals for frequency
                                scaleLabel: {display: true, labelString: 'Frequency'}
                            },
                        ]
                    }   
                }
    })

    let leaderboard = new Chart(CHART2, {
            type: 'horizontalBar',
            data: {
                labels: leaderslabel,
                datasets: [{
                    label: 'Leaderboard',
                    data: yaxis,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 206, 86, 0.2)',
                        'rgba(75, 192, 192, 0.2)',
                        'rgba(153, 102, 255, 0.2)',
                        'rgba(255, 159, 64, 0.2)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)',
                        'rgba(255, 159, 64, 1)'
                    ],
                    borderWidth: 1
                },]
            },
            options: {
                        scales: 
                        {
                        xAxes: 
                            [   
                                {
                                    display: false,
                                    barPercentage: 1.3,
                                    ticks: { max: 90,}
                                }, 
                                {
                                    display: true,
                                    ticks: {autoSkip: false,max: 100,},
                                    scaleLabel: {display: true, labelString: 'Score (%)'}
                                }
                            ],
                        yAxes: 
                            [
                                {
                                    ticks: {beginAtZero:true, precision:0   }, //precision 0 removes decimals for frequency
                                    scaleLabel: {display: true, labelString: 'Leaders'}
                                },
                            ]
                        }   
                    }
        })
    }