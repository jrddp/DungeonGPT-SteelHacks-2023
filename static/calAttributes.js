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

document.addEventListener('DOMContentLoaded', () => {
    const submit_button = document.getElementById('submit-button');
    submitButton.addEventListener('click', submitForm);
});
// dan wyd i redid this file
// can i replace it
// 
// Add this function to handle the form submission
// got u.
async function submitForm() {
    const playerName = document.getElementById('player_name').value;
    const playerDescription = document.getElementById('player_description').value;
    const strength = document.getElementById('strength').value;
    const dexterity = document.getElementById('dexterity').value;
    const constitution = document.getElementById('constitution').value;
    const intelligence = document.getElementById('intelligence').value;
    const wisdom = document.getElementById('wisdom').value;
    const charisma = document.getElementById('charisma').value;

    const attributeData = {};
    attributes.forEach(attr => {
        attributeData[attr] = parseInt(attributeValues[attr].innerText);
    });

    const data = {
        player_name: playerName,
        archetype: playerDescription,
        // attributes: attributeData
        strength: strength,
        dexterity: dexterity,
        constitution: constitution,
        intelligence: intelligence,
        wisdom: wisdom,
        charisma: charisma
    };

    try {
        const response = await fetch('/charater_creation', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            console.log('Form submitted successfully');
            response.json()
            .then(data => {
                console.log(data);
            })
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


