function initializeApp() {

    document.getElementById("search-button").addEventListener("click", function () {
        const userInput = document.getElementById("search-input").value;
        const responseLength = document.getElementById("response-length").value;
        // console.log("Inputs: ", userInput,", ", responseLength)
        validateInputLength(userInput)
        fetchAPIAndDisplayResult(userInput, responseLength);
    });
}

function validateInputLength(userInput) {
    if (userInput.length < 5) {
        errorMessage.style.display = "block";
        throw new Error('Input not long enough.');
    } else {
        errorMessage.style.display = "none";
    }
}

async function fetchAPIAndDisplayResult(inputText, responseLength) {
    if (!responseLength) {
        responseLength = 150;
    }
    const prompt = {
        text: inputText,
        response_length: parseInt(responseLength, 10)
    };
    const spinner = document.getElementById("spinner");
    spinner.style.display = "block";
    try {
        const response = await fetch('http://localhost/generate/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(prompt),
        });
        if (!response.ok) throw new Error('Network response was not ok.');

        const data = await response.json();

        spinner.style.display = "none";


        // Display the responses
        document.getElementById('LiberalResponse').innerText = data.liberal;
        document.getElementById('ConservativeResponse').innerText = data.conservative;
        document.getElementById('ConservativePrompt').innerText = data.prompt;
        document.getElementById('LiberalPrompt').innerText = data.prompt;
    } catch (error) {
        console.error('There has been a problem with the fetch:', error);
    }
}