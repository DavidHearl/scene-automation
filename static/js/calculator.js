// Check the JS file has loaded
// console.log("Calculator Loaded")

document.querySelector("#calculate-button").addEventListener("click", calculate);

function displayHTML() {
    const contentContainer = document.getElementById('dashboard-container');
    const htmlContent = `
        <div class="result-container">
            <canvas id="estimated-completion"></canvas>
        </div>

        <div class="dates">
            <div class="lower-date">
                <h3 class="est-completion">Earliest Completion</h3>
                <div class="data-container">
                    <span id="date-lower"></span>
                </div>
            </div>
            <div class="upper-date">
                <h3 class="est-completion">Estimated Completion</h3>
                <div class="data-container">
                    <span id="date-upper"></span>
                </div>
            </div>
        </div>

        <div class="storage-summary">
            <div class="storage-column">
                <div class="data-box">
                    <h3 class="est-completion">Raw Data Size:</h3>
                    <div class="data-container">
                        <span id="raw-data"></span>
                    </div>
                </div>
                <div class="data-box">
                    <h3 class="est-completion">Exported Data Size:</h3>
                    <div class="data-container">
                        <span id="exported-data"></span>
                    </div>
                </div>
            </div>
            <div class="storage-column">
                <div class="data-box">            
                    <h3 class="est-completion">Processed Data Size:</h3>
                    <div class="data-container">
                        <span id="processed-data"></span>
                    </div>
                </div>
                <div class="data-box special">
                    <h3 class="est-completion">Total Data Size:</h3>
                    <div class="data-container">
                        <span id="total-data"></span>
                    </div>
                </div>
            </div>
            <canvas id="totalDataPieChart"></canvas>
        </div>
    `;

    contentContainer.innerHTML = htmlContent;
}


function calculate() {
    displayHTML();

    // Verify the function has been called correctly
    // console.log("Calculate Function")

    // Get the current time till completion
    let currentTimeRemaining = document.querySelector("#total-time").innerHTML;
    currentTimeRemaining = Number(currentTimeRemaining);

    // Get the value from the calculator input
    const input = document.querySelector("#calculator-input").value;

    // Generate a random number between 30 and 25 for the number of scans per area
    let randomScansPerArea = Math.floor(Math.random() * (30 - 25 + 1)) + 25;
    // console.log("Random", randomScansPerArea)

    // Divide by the rough number of areas per ship, this is roughly 17.3
    var areas = Math.round(input/randomScansPerArea, 0);

    // Assign an empty array
    var scansPerArea = [];

    // Generate random values
    var sum = 0;
    for (var i = 0; i < areas - 1; i++) {
        var value;
        do {
            value = Math.max(1, Math.round(Math.abs(boxMullerRandom(input/areas, input/areas/2))));
        } while (value > input - sum - (areas - i - 1));
        sum += value;
        scansPerArea.push(value);
    }

    // Add the difference to the array as the last element
    scansPerArea.push(input - sum);
    // console.log(scansPerArea)

    totalTime = 0

    // Calculate time for each area
    for (let i = 0; i < scansPerArea.length; i++) {
        // Set the number of scans to the random value from the array and set time to 30 (time per area)
        let numberOfScans = scansPerArea[i]
        let time = 30

        let baseTime = 20 * numberOfScans
        let exponential = 1.006 ** numberOfScans

        let exponentialTime = baseTime * exponential

        time += exponentialTime

        let daysLeft = (time / 60) / 8

        totalTime += daysLeft
    }

    let averageRaw = document.querySelector("#averageRaw").innerHTML;
    let averageProcessed = document.querySelector("#averageProcessed").innerHTML;
    let averageExported = document.querySelector("#averageExported").innerHTML;

    averageRaw = parseFloat((averageRaw * input).toFixed(2));
    averageProcessed = parseFloat((averageProcessed * input).toFixed(2));
    averageExported = parseFloat((averageExported * input).toFixed(2));
    totalSize = parseFloat((averageRaw + averageProcessed + averageExported).toFixed(2));

    if (averageRaw >= 1000) {
        averageRaw = averageRaw / 1000;
        averageRaw = parseFloat(averageRaw.toFixed(2));
        rawExpression = "TB";
    } else {
        rawExpression = "GB"
    };

    if (averageProcessed >= 1000) {
        averageProcessed = averageProcessed / 1000;
        averageProcessed = parseFloat(averageProcessed.toFixed(2));
        processedExpression = "TB";
    } else {
        processedExpression = "GB"
    }

    if (averageExported >= 1000) {
        averageExported = averageExported / 1000;
        averageExported = parseFloat(averageExported.toFixed(2));
        exportedExpression = "TB";
    } else {
        exportedExpression = "GB"
    }

    if (totalSize >= 1000) {
        totalSize = totalSize / 1000;
        totalSize = parseFloat(totalSize.toFixed(2));
        totalExpression = "TB";
    } else {
        totalExpression = "GB"
    }

    document.querySelector("#raw-data").innerHTML = `<h2>${averageRaw} ${rawExpression}</h2>`;
    document.querySelector("#processed-data").innerHTML = `<h2>${averageProcessed} ${processedExpression}</h2>`;
    document.querySelector("#exported-data").innerHTML = `<h2>${averageExported} ${exportedExpression}</h2>`;
    document.querySelector("#total-data").innerHTML = `<h2>${totalSize} ${totalExpression}</h2>`;

    totalTime = Math.round(totalTime * 100) / 100;

    let lowerBound = totalTime * 1.2
    let upperBound = totalTime * 1.9

    lowerBound = Math.round(lowerBound * 100) / 100;
    upperBound = Math.round(upperBound * 100) / 100;

    // Create an upper and lower bound for the date
    lowerBoundPlusCurrent = lowerBound + currentTimeRemaining
    upperBoundPlusCurrent = upperBound + currentTimeRemaining

    const today = new Date();

    let lowerBoundDate = addWeekdays(today, lowerBoundPlusCurrent);
    let upperBoundDate = addWeekdays(today, upperBoundPlusCurrent);
    
    document.querySelector("#date-lower").innerHTML = `<h2>${lowerBoundDate.toDateString()}</h2>`;
    document.querySelector("#date-upper").innerHTML = `<h2>${upperBoundDate.toDateString()}</h2>`;

    // Estimated Time Chart
    // Calculate the difference between the upper and lower bounds
    let duration = upperBound - lowerBound;

    // Chart.js configuration
    const estconfig = {
        type: 'bar',
        data: {
            labels: ['Estimated Completion'], // Single category
            datasets: [{
                label: 'Minimum Days',
                data: [lowerBound], // Lower bound value
                backgroundColor: 'rgb(54, 162, 235)', // Example color
                stack: 'Stack 0', // Specify the stack
            }, {
                label: 'Estimated Additional Days',
                data: [duration], // Difference (upper - lower bound)
                backgroundColor: 'rgb(255, 99, 132)', // Example color
                stack: 'Stack 0', // Same stack to ensure they are stacked together
            }]
        },
        options: {
            indexAxis: 'y', // Horizontal bar chart
            scales: {
                x: {
                    stacked: true, // Enable stacking on the x-axis
                    ticks: {
                        color: 'white', // Change x-axis labels to white
                    },
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)', // Optional: change grid line colors
                    },
                },
                y: {
                    stacked: true, // Enable stacking on the y-axis
                    ticks: {
                        color: 'white', // Change y-axis labels to white
                    },
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)', // Optional: change grid line colors
                    },
                }
            },
            plugins: {
                legend: {
                    display: true, // Display legend (optional)
                    labels: {
                        color: 'white', // Change legend text to white
                    },
                },
                title: {
                    display: true,
                    text: 'Estimated Completion Time',
                    color: 'white', // Change title text to white
                },
            },
        },
    };

    // Assuming you have a <canvas> element with id="myChart"
    const ctx = document.getElementById('estimated-completion').getContext('2d');
    const myChart = new Chart(ctx, estconfig);



    // Pie Chart
    const data = {
        labels: [
            'Raw Data',
            'Processed Data',
            'Exported Data'
        ],
        datasets: [{
            label: 'Total Data Distribution',
            data: [averageRaw, averageProcessed, averageExported], // Use your calculated values here
            backgroundColor: [
                'rgb(255, 99, 132)',
                'rgb(54, 162, 235)',
                'rgb(255, 205, 86)'
            ],
            hoverOffset: 4
        }]
    };
    
    const config = {
        type: 'doughnut',
        data: data,
        options: {
            plugins: {
                legend: {
                    labels: {
                        color: 'white' // Change legend text color
                    }
                },
                tooltip: {
                    titleFont: {
                        size: 14,
                        weight: 'bold',
                        color: 'yellow' // Change tooltip title text color
                    },
                    bodyFont: {
                        size: 12,
                        color: 'lightblue' // Change tooltip body text color
                    }
                },
                title: { // Add this section to include a title
                    display: true,
                    text: 'Total Data Distribution', // Title text
                    color: 'white', // Title text color
                    font: {
                        size: 18,
                        weight: 'bold'
                    },
                    padding: {
                        top: 4,
                        bottom: 4
                    }
                }
            }
        }
    };
    
    // Render the pie chart
    const totalDataPieChart = new Chart(
        document.getElementById('totalDataPieChart'),
        config
    );
}

function addWeekdays(date, days) {
    date = new Date(date);
    let i = 0;
    while (i < days) {
        date.setDate(date.getDate() + 1);
        if (date.getDay() !== 0 && date.getDay() !== 6) {
            i++;
        }
    }
    return date;
}

function boxMullerRandom(mean, stdev) {
    let u = 0, v = 0;
    while(u === 0) u = Math.random(); //Converting [0,1) to (0,1)
    while(v === 0) v = Math.random();
    let num = Math.sqrt( -2.0 * Math.log( u ) ) * Math.cos( 2.0 * Math.PI * v );
    num = num * stdev + mean; // Translate to desired mean and stdev
    return num;
}
