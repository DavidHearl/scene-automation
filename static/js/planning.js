document.addEventListener('DOMContentLoaded', function() {
    const table = document.getElementById('area-planning-table');
    const rows = table.getElementsByClassName('table-row');
    const runningTotalElement = document.getElementById('running-total');
    const requiredTimeElement = document.getElementById('required-time');
    const requiredDaysElement = document.getElementById('required-days');
    const scannerRadios = document.getElementsByName('scanners');
    const qualityRadios = document.getElementsByName('quality');
    let runningTotal = 0;
    let scanners = 1;
    let quality = 'high';

    function updateRunningTotal() {
        runningTotalElement.textContent = `Scans: ${runningTotal}`;
        // quality either low or high
        // scanners either 1 or 2

        let scansPerHour;
        if (quality === 'high') {
            scansPerHour = 3600 / 455
            if (scanners == 2) {
                scansPerHour += 3600 / 661
            }
        } else {
            scansPerHour = 3600 / 234
            if (scanners == 2) {
                scansPerHour += 3600 / 279
            }
        }

        let scanTime = runningTotal / scansPerHour;
        requiredTimeElement.textContent = `Time Required: ${scanTime.toFixed(2)} Hours`;

        let scanDays = scanTime / 12
        requiredDaysElement.textContent = `Days Required: ${scanDays.toFixed(2)} Days`
    }

    function toggleRowSelection(row) {
        const avgScansCell = row.querySelector('.avg-scans');
        if (!avgScansCell) return; // Ensure avgScansCell is not null
        const avgScansValue = parseFloat(avgScansCell.textContent) || 0;
    
        row.classList.toggle('selected');
        if (row.classList.contains('selected')) {
            row.style.backgroundColor = 'purple';
            row.style.color = 'white';
            runningTotal += avgScansValue;
        } else {
            row.style.backgroundColor = '';
            row.style.color = '';
            runningTotal -= avgScansValue;
        }
    
        updateRunningTotal();
    }

    for (let row of rows) {
        row.addEventListener('click', function() {
            toggleRowSelection(this);
        });
    }

    // Add event listeners to the scanner radio buttons
    scannerRadios.forEach(radio => {
        radio.addEventListener('change', function() {
            scanners = parseInt(this.value);
            updateRunningTotal();
        });
    });

    // Add event listeners to the quality radio buttons
    qualityRadios.forEach(radio => {
        radio.addEventListener('change', function() {
            quality = this.value;
            updateRunningTotal();
        });
    });

    function updateMissingAreas() {
        const shipSelect = document.getElementById('ship-select');
        const selectedShipId = shipSelect.value;
        const missingAreas = document.getElementById('missing-areas');
        const hiddenAreaRow = document.getElementsByClassName('area-row');
        const mainAreaValue = document.getElementsByClassName('main-area-value');

        // Clear the current content of #missing-areas
        missingAreas.innerHTML = '<h3 class=small-title>Missing Areas</h3>';

        // Create arrays to store the areas
        const hiddenAreaArray = [];
        const mainAreaArray = [];
        const included = [];
        let missing = []; // Change const to let

        // Loop through all hidden areas and create an array
        for (let i = 0, len = hiddenAreaRow.length; i < len; i++) {
            // Get the Data cells in each row
            const cells = hiddenAreaRow[i].getElementsByTagName('td');

            // Check to see if the ship matched the data then add to an array.
            if (cells[0].textContent == selectedShipId) {
                hiddenAreaArray.push(cells[1].textContent);
            }
        }

        // Loop through all the main areas and create an array
        for (let i = 0, len = mainAreaValue.length; i < len; i++) {
            // Get the data from each cell
            let area = mainAreaValue[i].textContent;

            // Add the value to the array
            mainAreaArray.push(area);
        }

        // Check for included and missing areas
        hiddenAreaArray.forEach(area => {
            if (mainAreaArray.includes(area)) {
                included.push(area);
            } else {
                missing.push(area);
            }
        });

        // Look through the missing array, and change repeated values
        const toiletCount = missing.filter(area => /toilet|restroom/i.test(area)).length;
        const cabinCount = missing.filter(area => /cabin/i.test(area)).length;

        if (toiletCount > 0) {
            // Remove all instances of 'toilets' or 'restrooms' from the missing array
            missing = missing.filter(area => !/toilet|restroom/i.test(area));
            // Add the new formatted string to the missing array
            missing.push(`${toiletCount} x Toilets/Restrooms`);
        }

        if (cabinCount > 0) {
            // Remove all instances of 'cabin' from the missing array
            missing = missing.filter(area => !/cabin/i.test(area));
            // Add the new formatted string to the missing array
            missing.push(`${cabinCount} x Cabins`);
        }

        // Clear the current content of #missing-areas
        missingAreas.innerHTML = '<h3 class=small-title>Missing Areas</h3>';

        // Create a checkbox, p element, and number input for every value in the missing array
        missing.forEach(area => {
            const div = document.createElement('div');
            div.classList.add('flex-item'); // Add a class to the div
            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.classList.add('checkbox')
            const p = document.createElement('p');
            p.textContent = area;
            const numberInput = document.createElement('input');
            numberInput.type = 'number';
            numberInput.value = 0;
            numberInput.min = 0;
            numberInput.classList.add('number-input'); // Add a class to the number input
            div.appendChild(checkbox);
            div.appendChild(p);
            div.appendChild(numberInput);
            missingAreas.appendChild(div);

            // Add event listener to the checkbox
            checkbox.addEventListener('change', function() {
                if (this.checked) {
                    div.style.transition = 'opacity 5s';
                    div.style.opacity = '0';
                } else {
                    div.style.transition = 'none';
                    div.style.opacity = '1';
                }
            });

            // Remove the div when the transition ends and add to the table
            div.addEventListener('transitionend', function() {
                if (div.style.opacity === '0') {
                    const areaName = p.textContent;
                    const avgScansValue = numberInput.value;

                    // Create a new row in the table
                    const newRow = document.createElement('div');
                    newRow.classList.add('table-row'); // Add table-row class
                    newRow.innerHTML = `
                        <div class="table-cell area">
                            <p class="main-area-value">${areaName}</p>
                        </div>
                        <div class="table-cell occurrences"></div>
                        <div class="table-cell avg-scans">${avgScansValue}</div>
                        <div class="table-cell min-scans"></div>
                        <div class="table-cell max-scans"></div>
                    `;
                    table.appendChild(newRow);

                    // Add click event listener to the new row to toggle selection
                    newRow.addEventListener('click', function() {
                        toggleRowSelection(newRow);
                    });

                    // Highlight the new row
                    toggleRowSelection(newRow);

                    // Remove the div
                    div.remove();
                }
            });

            // Add event listener to the number input to update the running total
            numberInput.addEventListener('input', function() {
                const previousValue = parseFloat(numberInput.getAttribute('data-previous-value')) || 0;
                const newValue = parseFloat(numberInput.value) || 0;
                runningTotal += newValue - previousValue;
                numberInput.setAttribute('data-previous-value', newValue);
                updateRunningTotal();
            });
        });

        // Reset the state of all rows and the running total
        runningTotal = 0;
        for (let row of rows) {
            row.classList.remove('selected');
            row.style.backgroundColor = '';
            row.style.color = '';
        }

        // Simulate click on rows corresponding to included areas
        for (let row of rows) {
            const areaNameElement = row.querySelector('.main-area-value');
            if (areaNameElement) {
                const areaName = areaNameElement.textContent.trim();
                if (included.includes(areaName)) {
                    toggleRowSelection(row);
                }
            }
        }

        // Update the running total display
        updateRunningTotal();
    }

    // Attach the updateMissingAreas function to the change event of the ship-select element
    const shipSelect = document.getElementById('ship-select');
    shipSelect.addEventListener('change', updateMissingAreas);
});