document.addEventListener("DOMContentLoaded", function() {
  var languageStatsJson = document.getElementById('pie-chart').getAttribute('data-language-stats');
  var languageStats = JSON.parse(languageStatsJson);

  if (languageStats.length === 0) {
      var ctx = document.getElementById('pie-chart').getContext('2d');
      if (window.myPieChart != null) {
        window.myPieChart.destroy(); // Destroys the previous chart
    }
      var myPieChart = new Chart(ctx, {
          type: 'pie',
          data: {
              labels: ['No Data'],
              datasets: [{
                  data: [1], // Placeholder value
                  backgroundColor: ['grey'],
                  borderWidth: 0
              }]
          },
          options: {
              plugins:{
                title:{
                    display:true,
                    text:"solved problems by language"
                }

              },
              tooltips: {
                  callbacks: {
                      label: function(tooltipItem, data) {
                          return 'You haven\'t solved any problems yet!';
                      }
                  }
              }
          }
      });
  } else {
      var ctx = document.getElementById('pie-chart').getContext('2d');
      var myPieChart = new Chart(ctx, {
          type: 'pie',
          data: {
              labels: languageStats.map(stat => stat.language_name),
              datasets: [{
                  data: languageStats.map(stat => stat.num_problems_solved),
                  backgroundColor: [
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
                      'rgba(153, 102, 255, 1)'
                      
                  ],
                  borderWidth: 2
              }]
          },
          options: {
            
            plugins : {
              title: {
                display : true,
                
                text: "solved problems by language"
                
              },
              legend: {
                position: 'left',
                align: 'center'
              }

            }
          }
      });
  }
});
