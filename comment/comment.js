fetch("/api/comments?assetId=123")
  .then(response => response.json())
  .then(comments => displayComments(comments))
  .catch(error => console.error(error));
