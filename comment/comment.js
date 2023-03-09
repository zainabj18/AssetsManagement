const commentsList = document.getElementById("comments-list");
const commentForm = document.getElementById('comment-form');
const commentsArea = document.getElementById('comments');

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
  const li = document.createElement("li");
  li.innerHTML = `
    <div class="comment-author">${comment.name} (${comment.email})</div>
    <div class="comment-body">${comment.comment}</div>
    <div class="comment-metadata">
      <span class="comment-date">${new Date(comment.date).toLocaleString()}</span>
      <button class="comment-reply">Reply</button>
      <button class="comment-report">Report</button>
    </div>
  `;
  commentsList.appendChild(li);
}

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
