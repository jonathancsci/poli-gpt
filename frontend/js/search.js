console.log("hello");
function initializeApp() {

    document.getElementById("button-addon2").addEventListener("click", function() {
        const userInput = document.querySelector("input[type='text']").value;
        const num_articles = document.getElementById("responseLength").value;
        fetchAPIAndDisplayResult(userInput, num_articles);
    });
}

async function fetchAPIAndDisplayResult(inputText, num_articles) {
    const prompt = {
        text: inputText,
        num_articles: parseInt(num_articles, 10)
    };

    try {
        const response = await fetch('http://localhost/search/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(prompt),
        });

        if (!response.ok) throw new Error('Network response was not ok.');

        const data = await response.json();

        // Clear existing accordion items
        document.getElementById('liberalAccordionCol').innerHTML = '';
        document.getElementById('conservativeAccordionCol').innerHTML = '';

        // Display the responses in accordion format
        const liberal_Accordion = document.getElementById('liberalAccordionCol');
        const conservative_Accordion = document.getElementById('conservativeAccordionCol');

        if (data.liberal.length > 0) {
            const liberalAccordion = createAccordion(data.liberal, 'Liberal');
            liberal_Accordion.appendChild(liberalAccordion);
        }

        if (data.conservative.length > 0) {
            const conservativeAccordion = createAccordion(data.conservative, 'Conservative');
            conservative_Accordion.appendChild(conservativeAccordion);
        }
    } catch (error) {
        console.error('There has been a problem with the fetch:', error);
    }
}

function createAccordion(articles, category) {
    const accordion = document.createElement('div');
    accordion.className = 'accordion';
    accordion.id = category


    articles.forEach((article, index) => {
        const accordionItem = document.createElement('div');
        accordionItem.className = 'accordion-item';

        const headerId = `${category}-${index}`;
        const collapseId = `collapse-${category}-${index}`;

        const header = `
            <h2 class="accordion-header" id="${headerId}">
                <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#${collapseId}" aria-expanded="false" aria-controls="${collapseId}">
                    ${article.headline}
                </button>
            </h2>
        `;

        const collapse = `
            <div id="${collapseId}" class="accordion-collapse collapse" aria-labelledby="${headerId}" data-bs-parent="#accordionExample">
                <div class="accordion-body">
                    ${article.body}
                    <a href="${article.url}" target="_blank">Read more</a>
                </div>
            </div>
        `;

        accordionItem.innerHTML = header + collapse;
        accordion.appendChild(accordionItem);
    });

    return accordion;
}