document.addEventListener('DOMContentLoaded', () => {
    const attributes =    ['strength', 'dexterity', 'constitution', 'intelligence', 'wisdom', 'charisma'];
    const attributeInputs = {};
    const attributeValues = {};
    const totalAttributePoints = document.getElementById('total-attribute-points');
    let currentTotal = 0;

    function updateAttributes() {
        currentTotal = 0;
        attributes.forEach(attr => {
            currentTotal += parseInt(attributeValues[attr].innerText);
        });
        totalAttributePoints.innerText = currentTotal;
    }

    function adjustSliders() {
        const availablePoints = 15 - currentTotal;
        attributes.forEach(attr => {
            const currentValue = parseInt(attributeValues[attr].innerText);
            attributeInputs[attr].max = Math.min(5, currentValue + availablePoints);
        });
    }

    attributes.forEach(attr => {
        const input = document.getElementById(attr);
        const value = document.getElementById(`${attr}-value`);

        input.addEventListener('input', () => {
            value.innerText = input.value;
            updateAttributes();
            adjustSliders();
        });

        attributeInputs[attr] = input;
        attributeValues[attr] = value;
    });

    updateAttributes();
    adjustSliders();
});


// Add this function to handle the form submission
async function submitForm() {
    const playerName = document.getElementById('player_name').value;
    const playerDescription = document.getElementById('player_description').value;

    const attributeData = {};
    attributes.forEach(attr => {
        attributeData[attr] = parseInt(attributeValues[attr].innerText);
    });

    const data = {
        player_name: playerName,
        player_description: playerDescription,
        attributes: attributeData
    };

    try {
        const response = await fetch('/your-endpoint', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            console.log('Form submitted successfully');
        } else {
            console.error('Error submitting form:', response.statusText);
        }
    } catch (error) {
        console.error('Error submitting form:', error);
    }
}


// Add event listener for submit button
const submitButton = document.getElementById('submit-button');
submitButton.addEventListener('click', submitForm);


