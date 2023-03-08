const commentForm = document.getElementById('comment-form');
const commentsArea = document.getElementById('comments');

// Handle form submission
commentForm.addEventListener('submit', (e) => {
  e.preventDefault();

  const name = document.getElementById('name').value;
  const email = document.getElementById('email').value;
  const comment = document.getElementById('comment').value;

  // Send HTTP request to API endpoint to save comment data
  fetch('/api/comments', {
    method: 'POST',
    body: JSON.stringify({ name, email, comment }),
    headers: { 'Content-Type': 'application/json' }
  })
  .then(response => response.json())
  .then(data => {
    // Display newly added comment
    displayComment(data);
  })
  .catch(error => {
    console.error(error);
    // Handle error gracefully
  });
});

// Retrieve existing comments on page load
fetch('/api/comments')
  .then(response => response.json())
  .then(data => {
    // Display all comments
    data.forEach(comment => displayComment(comment));
  })
  .catch(error => {
    console.error(error);
    // Handle error gracefully
  });

// Display a single comment in the UI
function displayComment(comment) {
  const commentDiv = document.createElement('div');
  commentDiv.innerHTML = `
    <h3>${comment.name}</h3>
    <p>${comment.comment}</p>
    <p><em>${comment.email}</em></p>
  `;
  commentsArea.appendChild(commentDiv);
}
