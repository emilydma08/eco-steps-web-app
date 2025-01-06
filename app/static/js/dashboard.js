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

            // Reset the "Today's Challenge" section
            todaysChallengeContainer.innerHTML = '<p>No challenge selected</p>';

            // Update the progress circle
            updateProgress();
        },
        { once: true } // Ensure this listener runs only once
    );
}

// Function to update progress
function updateProgress() {
    // Calculate progress as a percentage
    const progress = (completedChallenges / totalChallenges) * 100;

    // Update the progress circle
    progressCircle.style.background = `
        conic-gradient(
            #8CC2A5 ${progress}%, 
            lightgray ${progress}%
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
