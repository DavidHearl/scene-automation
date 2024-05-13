console.log("Calculator Loaded")

document.querySelector("#calculate-button").addEventListener("click", calculate);

function calculate() {
    // Verify the function has been called correctly
    console.log("Calculate Function")

    // Get the value from the calculator input
    const input = document.querySelector("#calculator-input").value;

    result = input

    lowerBound = input * 0.75
    upperBound = input * 1.25

    document.querySelector("#result").innerHTML = `<h2>${ lowerBound } Days - ${ upperBound } Days</h2>`;
}

