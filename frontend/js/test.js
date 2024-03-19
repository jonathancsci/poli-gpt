console.log("hello");
 function initializeApp() {
        document.getElementById("button-addon2").addEventListener("click", function() {
            const userInput = document.querySelector("input[type='text']").value;
            const responseLength = document.getElementById("responseLength").value; 
            fetchAPIAndDisplayResult(userInput, responseLength);
        });
    }
    
    async function fetchAPIAndDisplayResult(inputText, responseLength) {
        const prompt = {
            text: inputText,
            response_length: parseInt(responseLength, 10)
        };
    
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
    
            // Display the responses
            document.getElementById('LiberalResponse').innerText = data.liberal;
            document.getElementById('ConservativeResponse').innerText = data.conservative;
            document.getElementById('ConservativePrompt').innerText = data.prompt;
            document.getElementById('LiberalPrompt').innerText = data.prompt;
        } catch (error) {
            console.error('There has been a problem with the fetch:', error);
        }
    }