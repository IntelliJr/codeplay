document.addEventListener("DOMContentLoaded", function () {
    // Get data from HTML attributes
    var difficultyStats = JSON.parse(document.getElementById('bar-chart').getAttribute('data-difficulty-stats'));

    if(difficultyStats.length === 0){
        var ctx = document.getElementById('bar-chart').getContext('2d');
        if (window.myChart != null) {
            window.myChart.destroy(); // Destroys the previous chart
        }
        
        var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ["No Data"],
            datasets: [{
                data: [1],
                backgroundColor:"grey"

            }]
        },
        options: {
            plugins: {
                title:{
                    display:true,
                    text: "solved problems by difficulty"

                }

            },
            tooltips: {
                mode: 'index',
                intersect: false
            },
            scales: {
                x:{
                    stacked:true
                },
                y:{
                    stacked:true,
                    ticks:{
                        stepSize: 1
                    }

                }
               
            }
        }
    });

    }
        // Process data for the chart
    var labels = {}; // Language labels
    var data = {}; // Data for each difficulty level

    // Initialize data objects
    difficultyStats.forEach(function (stat) {
        if (!labels[stat.language_name]) {
            labels[stat.language_name] = true;
            data[stat.language_name] = {
                easy: 0,
                medium: 0,
                hard: 0
            };
        }

        // Increment count based on difficulty level
        switch (stat.difficulty_level) {
            case 'Easy':
                data[stat.language_name].easy++;
                break;
            case 'Medium':
                data[stat.language_name].medium++;
                break;
            case 'Hard':
                data[stat.language_name].hard++;
                break;
        }
    });

    // Create the stacked bar chart
    var ctx = document.getElementById('bar-chart').getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'bar',
        
        data: {
            labels: Object.keys(labels),
            datasets: [{
                label: 'Easy',
                data: Object.values(data).map(obj => obj.easy),
                backgroundColor: 'rgba(75, 192, 192, 0.5)'
            }, {
                label: 'Medium',
                data: Object.values(data).map(obj => obj.medium),
                backgroundColor: 'rgba(255, 206, 86, 0.5)'
            }, {
                label: 'Hard',
                data: Object.values(data).map(obj => obj.hard),
                backgroundColor: 'rgba(255, 99, 132, 0.5)'
            }]
        },
        options: {
            plugins: {
                title:{
                    display:true,
                    text: "solved problems by difficulty"

                }

            },
            tooltips: {
                mode: 'index',
                intersect: false
            },
            scales: {
                x:{
                    stacked:true
                },
                y:{
                    stacked:true,
                    ticks:{
                        stepSize: 1
                    }

                }
               
            }
        }
    });
});
