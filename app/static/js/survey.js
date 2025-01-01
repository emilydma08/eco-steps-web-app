// Wait for the DOM to load
document.addEventListener('DOMContentLoaded', function () {

    // Select the survey form and the submit button
    const surveyForm = document.getElementById('survey-form');
    const submitButton = surveyForm.querySelector('button[type="submit"]');

    // When the user clicks submit, run the validation and process logic
    surveyForm.addEventListener('submit', function (e) {
        e.preventDefault();  // Prevent the form from submitting immediately

        // Validate that all required fields are filled
        let isValid = true;

        // Check if required radio buttons are selected
        const requiredRadioGroups = surveyForm.querySelectorAll('input[required][type="radio"]');
        requiredRadioGroups.forEach(group => {
            const name = group.name;
            if (!surveyForm.querySelector(`input[name="${name}"]:checked`)) {
                isValid = false;
            }
        });

        // Check if required range inputs are filled (this is for lifestyle rating)
        const requiredRangeInputs = surveyForm.querySelectorAll('input[required][type="range"]');
        requiredRangeInputs.forEach(input => {
            if (input.value === "") {
                isValid = false;
            }
        });

        // Check if required text inputs are filled
        const requiredTextInputs = surveyForm.querySelectorAll('input[required][type="text"]');
        requiredTextInputs.forEach(input => {
            if (input.value.trim() === "") {
                isValid = false;
            }
        });

        // If form is valid, submit the data to the server
        if (isValid) {
            // Collect the data
            const formData = new FormData(surveyForm);
            const data = {};

            formData.forEach((value, key) => {
                data[key] = value;
            });

            // Send the data to the backend (Flask)
            fetch('/survey', {
                method: 'POST',
                body: JSON.stringify(data),
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => {
                if (response.ok) {
                    // If the response is OK, handle the redirect to the campaigns page
                    window.location.href = '/campaigns';
                } else {
                    // Handle unexpected server responses
                    alert('Error: Unable to process the form submission.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('There was an error processing your form.');
            });
        } else {
            alert('Please fill in all required fields before submitting.');
        }
    });
});
