// Select all elements with the class 'booking-card'
var bookingCards = document.querySelectorAll('.booking-card');

// Function to generate dates between two dates
function getDatesBetween(startDate, endDate) {
    var dates = [];
    var currentDate = new Date(startDate);
    var end = new Date(endDate);

    while (currentDate <= end) {
        dates.push(currentDate.toISOString().split('T')[0]);
        currentDate.setDate(currentDate.getDate() + 1);
    }

    return dates;
}

// Iterate over each booking card
bookingCards.forEach(function(card) {
    // Select the element with the class 'booking-ship' within the current card
    var bookingShipElement = card.querySelector('.booking-ship');
    var bookingShipText = bookingShipElement ? bookingShipElement.textContent : null;

    // Select the input fields within the current card
    var inputFields = card.querySelectorAll('input');
    var dateValues = Array.from(inputFields).map(function(input) {
        return input.value;
    }).filter(function(value) {
        // Regular expression to match date format YYYY-MM-DD
        return /^\d{4}-\d{2}-\d{2}$/.test(value);
    });

    if (dateValues.length >= 2) {
        var startDate = dateValues[0];
        var endDate = dateValues[1];
        var allDates = getDatesBetween(startDate, endDate);
        dateValues = allDates;
    }

    // Select the select box within the current card
    var scannerSelectElement = card.querySelector('select');
    var scannerValue = scannerSelectElement ? scannerSelectElement.value : null;

    // Combine all data into an array
    var combinedData = [bookingShipText, scannerValue].concat(dateValues);

    // Log the combined data to the console (optional)
    console.log('Combined Data:', combinedData);
});