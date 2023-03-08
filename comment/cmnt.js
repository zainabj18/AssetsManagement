// Sample API endpoint for handling comment submissions
app.post('/api/comments', (req, res) => {
  const { name, email, comment } = req.body;
  const newComment = { name, email, comment };

  // Save new comment to database
  db.comments.insertOne(newComment, (err, result) => {
    if (err) {
      console.error(err);
      return res.status(500).send('Error saving comment');
    }

    // Return newly added comment
    res.json(result.ops[0]);
  });
});
