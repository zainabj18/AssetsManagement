<div id="comments-container">
  <h2>Comments</h2>
  <ul id="comments-list"></ul>
  <div id="comments-pagination"></div>
  <form id="comment-form">
    <input type="text" name="name" placeholder="Name">
    <input type="email" name="email" placeholder="Email">
    <textarea name="comment" placeholder="Add a comment"></textarea>
    <button type="submit">Submit</button>
  </form>
</div>	




const commentsList = document.getElementById("comments-list");

function displayComments(comments) {
  commentsList.innerHTML = "";
  comments.forEach(comment => {
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
  });
}
