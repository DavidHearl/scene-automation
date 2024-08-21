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

            if (hoveredDate) {
                allBookings.forEach(function(booking) {
                    if (booking.includes(hoveredDate)) {
                        var scannerType = booking[1];
                        
                        // Determine which mark to highlight
                        var hoveredClass = hoveredElement.classList.contains('red') ? 'red' : 'blue';

                        // Highlight only dates in this booking and with the correct mark
                        var bookingDates = booking.slice(2);
                        highlightDates(bookingDates, scannerType, true, hoveredClass);
                        
                        document.getElementById('booking-summary').style.display = 'flex';
                    }
                });
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

            if (hoveredDate) {
                allBookings.forEach(function(booking) {
                    if (booking.includes(hoveredDate)) {
                        var scannerType = booking[1];
                        
                        // Determine which mark to unhighlight
                        var hoveredClass = hoveredElement.classList.contains('red') ? 'red' : 'blue';

                        // Unhighlight only dates in this booking and with the correct mark
                        var bookingDates = booking.slice(2);
                        highlightDates(bookingDates, scannerType, false, hoveredClass);
                        
                        setTimeout(function() {
                            document.getElementById('booking-summary').style.display = 'none';
                        }, 1000);
                    }
                });
            }
        }
    }
});
