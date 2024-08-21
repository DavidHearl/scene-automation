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

var allBookings = [];

// Iterate over each booking card
bookingCards.forEach(function(card) {
    var bookingShipElement = card.querySelector('.booking-ship');
    var bookingShipText = bookingShipElement ? bookingShipElement.textContent : null;

    var inputFields = card.querySelectorAll('input');
    var dateValues = Array.from(inputFields).map(function(input) {
        return input.value;
    }).filter(function(value) {
        return /^\d{4}-\d{2}-\d{2}$/.test(value);
    });

    if (dateValues.length >= 2) {
        var startDate = dateValues[0];
        var endDate = dateValues[1];
        var allDatesBetween = getDatesBetween(startDate, endDate);
        dateValues = allDatesBetween;
    }

    var scannerSelectElement = card.querySelector('select');
    var scannerValue = scannerSelectElement ? scannerSelectElement.value : null;

    var combinedData = [bookingShipText, scannerValue].concat(dateValues);

    allBookings.push(combinedData);
});

function highlightDates(dates, scanner, add, hoveredClass) {
    dates.forEach(function(date) {
        var dateElement = document.getElementById(date);
        if (dateElement) {
            if (scanner === 'red' || scanner === 'both') {
                var redMarks = dateElement.querySelectorAll('.red-booking-mark.red');
                redMarks.forEach(function(redMark) {
                    if (redMark.classList.contains(hoveredClass)) {
                        if (add) {
                            redMark.classList.add('active');
                        } else {
                            redMark.classList.remove('active');
                        }
                    }
                });
            }
            if (scanner === 'blue' || scanner === 'both') {
                var blueMarks = dateElement.querySelectorAll('.blue-booking-mark.blue');
                blueMarks.forEach(function(blueMark) {
                    if (blueMark.classList.contains(hoveredClass)) {
                        if (add) {
                            blueMark.classList.add('active');
                        } else {
                            blueMark.classList.remove('active');
                        }
                    }
                });
            }
        }
    });
}

let hideTimeout;

document.addEventListener('mouseover', function(event) {
    var hoveredElement = event.target;
    var parentElement = hoveredElement.closest('.day');

    if (parentElement) {
        var dateText = parentElement.querySelector('.date-text');
        if (dateText) {
            dateText.style.zIndex = -1;
        }

        if (hoveredElement.classList.contains('red-booking-mark') || 
            hoveredElement.classList.contains('blue-booking-mark')) {
            
            var hoveredDate = parentElement.id;
            var hoveredClass = hoveredElement.classList.contains('red') ? 'red' : 'blue';

            if (hoveredDate) {
                for (let booking of allBookings) {
                    if (booking.includes(hoveredDate)) {
                        var scannerType = booking[1];
                        
                        // Only proceed if the scanner type matches the hovered mark's color or if it applies to both
                        if ((hoveredClass === 'red' && (scannerType === 'red' || scannerType === 'both')) ||
                            (hoveredClass === 'blue' && (scannerType === 'blue' || scannerType === 'both'))) {
                            
                            // Highlight only dates in this booking with the correct mark
                            var bookingDates = booking.slice(2);
                            highlightDates(bookingDates, scannerType, true, hoveredClass);
                            
                            // Populate the template values
                            document.getElementById('ship-name').textContent = booking[0];
                            document.getElementById('start-date').textContent = bookingDates[0];
                            document.getElementById('end-date').textContent = bookingDates[bookingDates.length - 1];
                            document.getElementById('scanner').className = scannerType;

                            document.getElementById('booking-summary').style.display = 'flex';

                            // Clear any existing timeout to prevent hiding the summary
                            clearTimeout(hideTimeout);

                            // Check if the hoveredElement has the corresponding class before adding 'active'
                            if (hoveredElement.classList.contains(hoveredClass)) {
                                hoveredElement.classList.add('active');
                            }

                            // Stop processing further bookings since we've handled the first match
                            break;
                        }
                    }
                }
            }
        }
    }
});

document.addEventListener('mouseout', function(event) {
    var hoveredElement = event.target;
    var parentElement = hoveredElement.closest('.day');

    if (parentElement) {
        var dateText = parentElement.querySelector('.date-text');
        if (dateText) {
            dateText.style.zIndex = '';
        }

        if (hoveredElement.classList.contains('red-booking-mark') || 
            hoveredElement.classList.contains('blue-booking-mark')) {
            
            var hoveredDate = parentElement.id;
            var hoveredClass = hoveredElement.classList.contains('red') ? 'red' : 'blue';

            if (hoveredDate) {
                for (let booking of allBookings) {
                    if (booking.includes(hoveredDate)) {
                        var scannerType = booking[1];

                        // Only remove highlight if the scanner type matches the hovered mark's color or if it applies to both
                        if ((hoveredClass === 'red' && (scannerType === 'red' || scannerType === 'both')) ||
                            (hoveredClass === 'blue' && (scannerType === 'blue' || scannerType === 'both'))) {

                            // Remove highlight from all dates in the booking
                            var bookingDates = booking.slice(2);
                            highlightDates(bookingDates, scannerType, false, hoveredClass);

                            // Remove active class from the hovered element if it has the correct class
                            if (hoveredElement.classList.contains(hoveredClass)) {
                                hoveredElement.classList.remove('active');
                            }

                            break; // Stop processing further bookings
                        }
                    }
                }
            }
        }
    }
});
