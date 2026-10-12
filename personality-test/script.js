const form = document.getElementById('question-form');
const submitButton = document.getElementById('submit');
const overlay = document.getElementById('result-overlay');
const closeButton = document.getElementById('close-modal');
const retakeButton = document.getElementById('retake');

// Enable Submit once an answer is picked
form.addEventListener('change', () => {
	submitButton.disabled = false;
});

// Show the results pop-up (every answer gets the same diagnosis)
form.addEventListener('submit', (event) => {
	event.preventDefault();
	overlay.hidden = false;
	closeButton.focus();
});

function closeModal() {
	overlay.hidden = true;
	submitButton.focus();
}

closeButton.addEventListener('click', closeModal);

overlay.addEventListener('click', (event) => {
	if (event.target === overlay) {
		closeModal();
	}
});

document.addEventListener('keydown', (event) => {
	if (event.key === 'Escape' && !overlay.hidden) {
		closeModal();
	}
});

retakeButton.addEventListener('click', () => {
	form.reset();
	submitButton.disabled = true;
	overlay.hidden = true;
});
