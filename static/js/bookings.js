var bookingCards = document.querySelectorAll('.booking-card');

// Function to get dates between two dates
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

var bookingCards = document.querySelectorAll('.booking-card');
var allBookings = [];

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
        var allDatesBetween = getDatesBetween(startDate, endDate);
        dateValues = allDatesBetween;
    }

    // Select the select box within the current card
    var scannerSelectElement = card.querySelector('select');
    var scannerValue = scannerSelectElement ? scannerSelectElement.value : null;

    // Combine all data into an array
    var combinedData = [bookingShipText, scannerValue].concat(dateValues);

    // Add the combined data to the allBookings array
    allBookings.push(combinedData);
    print(combinedData);
});


// Function to highlight dates
function highlightDates(dates, scanner, add) {
    dates.forEach(function(date) {
        var dateElement = document.getElementById(date);
        if (dateElement) {
            if (scanner === 'red' || scanner === 'both') {
                var redMark = dateElement.querySelector('.red-booking-mark.red');
                if (redMark) {
                    if (add) {
                        redMark.classList.add('active');
                    } else {
                        redMark.classList.remove('active');
                    }
                }
            }
            if (scanner === 'blue' || scanner === 'both') {
                var blueMark = dateElement.querySelector('.blue-booking-mark.blue');
                if (blueMark) {
                    if (add) {
                        blueMark.classList.add('active');
                    } else {
                        blueMark.classList.remove('active');
                    }
                }
            }
        }
    });
}

// Add a global event listener for mouseover to log the ID of the hovered element or its parent
document.addEventListener('mouseover', function(event) {
    var hoveredElement = event.target;
    var parentElement = hoveredElement.closest('.day');

    if (parentElement) {
        // Set z-index of .date-text to negative on hover
        var dateText = parentElement.querySelector('.date-text');
        if (dateText) {
            dateText.style.zIndex = -1;
        }

        if (hoveredElement.classList.contains('red-booking-mark') || 
            hoveredElement.classList.contains('blue-booking-mark')) {
            
            var elementToLog = hoveredElement.classList.contains('day') ? hoveredElement : parentElement;
            
            if (elementToLog && elementToLog.id) {
                var hoveredDate = elementToLog.id;
                console.log('Hovered Date:', hoveredDate);

                // Check if the hovered date is present in any of the arrays
                allBookings.forEach(function(booking) {
                    if (booking.includes(hoveredDate)) {
                        // Determine which mark to highlight based on the hovered element
                        var scannerType = 'both';
                        if (hoveredElement.classList.contains('red-booking-mark') && hoveredElement.classList.contains('red')) {
                            scannerType = 'red';
                        } else if (hoveredElement.classList.contains('blue-booking-mark') && hoveredElement.classList.contains('blue')) {
                            scannerType = 'blue';
                        } else {
                            return; // Skip highlighting if the mark does not have the appropriate class
                        }
                        // Highlight all dates in the booking based on the scanner type
                        highlightDates(booking.slice(2), scannerType, true);
                    }
                });
            }
        }
    }
});

// Add a global event listener for mouseout to remove the .active class
document.addEventListener('mouseout', function(event) {
    var hoveredElement = event.target;
    var parentElement = hoveredElement.closest('.day');

    if (parentElement) {
        // Reset z-index of .date-text to its original value on mouseout
        var dateText = parentElement.querySelector('.date-text');
        if (dateText) {
            dateText.style.zIndex = '';
        }

        if (hoveredElement.classList.contains('red-booking-mark') || 
            hoveredElement.classList.contains('blue-booking-mark')) {
            
            var elementToLog = hoveredElement.classList.contains('day') ? hoveredElement : parentElement;
            
            if (elementToLog && elementToLog.id) {
                var hoveredDate = elementToLog.id;
                console.log('Hovered Date:', hoveredDate);

                // Check if the hovered date is present in any of the arrays
                allBookings.forEach(function(booking) {
                    if (booking.includes(hoveredDate)) {
                        // Determine which mark to remove highlight based on the hovered element
                        var scannerType = 'both';
                        if (hoveredElement.classList.contains('red-booking-mark') && hoveredElement.classList.contains('red')) {
                            scannerType = 'red';
                        } else if (hoveredElement.classList.contains('blue-booking-mark') && hoveredElement.classList.contains('blue')) {
                            scannerType = 'blue';
                        } else {
                            return; // Skip removing highlight if the mark does not have the appropriate class
                        }
                        // Remove highlight from all dates in the booking based on the scanner type
                        highlightDates(booking.slice(2), scannerType, false);
                    }
                });
            }
        }
    }
});