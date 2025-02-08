// DOM Elements
const todaysChallengeContainer = document.querySelector('#todays-challenge-container');
const allChallengesContainer = document.querySelector('#all-challenges');
const progressCircle = document.querySelector('.progress-circle');
const progressText = document.querySelector('.progress-text');

// Static total challenges count (captured once when the page loads)
const totalChallenges = document.querySelectorAll('#all-challenges .challenge').length;
let completedChallenges = 0; // Tracks the number of completed challenges

// Function to select a challenge
function selectChallenge(event) {
    const challengeDiv = event.target.closest('.challenge');

    // Check if a challenge is already selected in "Today's Challenge"
    const currentChallenge = todaysChallengeContainer.querySelector('.challenge');
    if (currentChallenge) {
        alert('Only one challenge can be selected at a time. Please complete the current one first.');
        return;
    }

    // Move the selected challenge to "Today's Challenge"
    todaysChallengeContainer.innerHTML = ''; // Clear placeholder text
    challengeDiv.classList.add('fade-in');
    todaysChallengeContainer.appendChild(challengeDiv);

    // Replace "Select" button with "Complete" checkbox
    const completeCheckbox = document.createElement('input');
    completeCheckbox.type = 'checkbox';
    completeCheckbox.className = 'complete-challenge';
    completeCheckbox.addEventListener('change', completeChallenge);

    challengeDiv.querySelector('.select-challenge').replaceWith(completeCheckbox);

    const deselectButton = document.createElement('button');
    deselectButton.textContent = 'Deselect';
    deselectButton.className = 'deselect-challenge';
    deselectButton.addEventListener('click', deselectChallenge);

    // Append the Deselect button to the challenge
    challengeDiv.appendChild(deselectButton);
}

// Function to deselect a challenge
function deselectChallenge(event) {
    // Find the challenge div
    const challengeDiv = event.target.closest('.challenge');

    // Remove the "Deselect" button
    const deselectButton = challengeDiv.querySelector('.deselect-challenge');
    if (deselectButton) {
        deselectButton.remove();
    }

    // Replace the "Complete" checkbox with the "Select" button
    const completeCheckbox = challengeDiv.querySelector('.complete-challenge');
    if (completeCheckbox) {
        const selectButton = document.createElement('button');
        selectButton.textContent = 'Select'; // Set button text
        selectButton.className = 'select-challenge'; // Add class for styling
        selectButton.addEventListener('click', selectChallenge); // Reattach event listener
        completeCheckbox.replaceWith(selectButton); // Replace the checkbox
    }

    // Move the challenge back to "All Challenges"
    allChallengesContainer.appendChild(challengeDiv);

    // Reset the "Today's Challenge" section
    todaysChallengeContainer.innerHTML = '<p>No challenge selected</p>';

    // Remove any animation classes
    challengeDiv.classList.remove('fade-in');
}


// Function to complete a challenge
function completeChallenge(event) {
    const challengeDiv = event.target.closest('.challenge');

    // Add fade-out class
    challengeDiv.classList.add('fade-out');

    // Wait for the transition to complete before removing the element
    challengeDiv.addEventListener(
        'transitionend',
        () => {
            // Remove the faded-out challenge
            challengeDiv.remove();

            // Increment the completed challenge counter
            completedChallenges++;
            checkCampaignCompletion();

            // Reset the "Today's Challenge" section
            todaysChallengeContainer.innerHTML = '<p>No challenge selected</p>';

            // Update the progress circle
            updateProgress();
        },
        { once: true } // Ensure this listener runs only once
    );
}

function showCelebrationPopup(){
    const popup = document.getElementById('celebration-popup');
    popup.classList.remove('hidden'); // Show the popup
}

// Attach an event listener to close the popup
document.getElementById('close-popup').addEventListener('click', () => {
    const popup = document.getElementById('celebration-popup');
    popup.classList.add('hidden'); // Hide the popup 

    // Reload the page to load the next campaign
    location.reload();
});

function checkCampaignCompletion(){
    const remainingChallenges = allChallengesContainer.querySelectorAll('.challenge').length;
    const activeChallenge = todaysChallengeContainer.querySelector('.challenge');

    if (remainingChallenges === 0 && !activeChallenge) {
        // Notify the server that the campaign is complete
        completeCampaign();
    }
}

function completeCampaign(){
    fetch('/complete_campaign', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ completed: true }),
    })
        .then(response => {
            if (response.ok) {
                // Reload the dashboard to load the next campaign
                showCelebrationPopup();
            } else {
                console.error('Error completing campaign');
            }
        })
        .catch(error => console.error('Error:', error));
}

// Function to update progress
function updateProgress() {
    // Calculate progress as a percentage
    const progress = (completedChallenges / totalChallenges) * 100;

    // Update the progress circle
    progressCircle.style.background = `
        conic-gradient(
            rgba(124, 144, 119) ${progress}%, 
            rgb(252, 248, 241) ${progress}%
        )
    `;

    // Update the progress text
    progressText.textContent = `${completedChallenges}/${totalChallenges} days`;

    // Check if all challenges are completed and update the message
    const remainingChallenges = allChallengesContainer.querySelectorAll('.challenge').length;

    // Check if there are no remaining challenges and display the message
    if (remainingChallenges === 0 && !todaysChallengeContainer.querySelector('.challenge')) {
        allChallengesContainer.innerHTML = '<p style="font-style: italic; color: gray;">No challenges remaining</p>';
    }
}

// Set initial progress text on page load
progressText.textContent = `0/${totalChallenges} days`;

// Attach event listeners to initial "Select" buttons
document.querySelectorAll('.select-challenge').forEach(button => {
    button.addEventListener('click', selectChallenge);
});

document.addEventListener("DOMContentLoaded", () => {
    // Get references to the elements
    const totalCampaignsCompletedElement = document.getElementById("total-campaigns-completed");
    const totalChallengesCompletedElement = document.getElementById("total-challenges-completed");

    // Populate the elements with the data passed from Flask
    totalCampaignsCompletedElement.textContent = totalCampaignsCompleted;
    totalChallengesCompletedElement.textContent = totalChallengesCompleted;
});

