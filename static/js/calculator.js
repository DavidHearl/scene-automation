// Check the JS file has loaded
// console.log("Calculator Loaded")

document.querySelector("#calculate-button").addEventListener("click", calculate);

function calculate() {
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

    totalTime = Math.round(totalTime * 100) / 100;

    let lowerBound = totalTime * 1.25
    let upperBound = totalTime * 1.75

    lowerBound = Math.round(lowerBound * 100) / 100;
    upperBound = Math.round(upperBound * 100) / 100;

    // Add the result to the HTML
    document.querySelector("#result-lower").innerHTML = `<h2>${ lowerBound } <i class="fa-solid fa-left-right"></i> </h2>`;
    document.querySelector("#result-upper").innerHTML = `<h2>${ upperBound }Days </h2>`;

    // Create an upper and lower bound for the date
    lowerBoundPlusCurrent = lowerBound + currentTimeRemaining
    upperBoundPlusCurrent = upperBound + currentTimeRemaining

    const today = new Date();

    let lowerBoundDate = addWeekdays(today, lowerBoundPlusCurrent);
    let upperBoundDate = addWeekdays(today, upperBoundPlusCurrent);
    
    document.querySelector("#date-lower").innerHTML = `<h2>${lowerBoundDate.toDateString()} <i class="fa-solid fa-left-right"></i> </h2>`;
    document.querySelector("#date-upper").innerHTML = `<h2>${upperBoundDate.toDateString()}</h2>`;
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