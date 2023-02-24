import { useState } from 'react';
import { Box, FormControl, FormLabel, Input, Textarea, Button } from '@chakra-ui/react';

function CommentForm({ onSubmit }) {
  const [username, setUsername] = useState('');
  const [content, setContent] = useState('');

  const handleSubmit = (event) => {
    event.preventDefault();
    const comment = { username, content };
    onSubmit(comment);
    setUsername('');
    setContent('');
  };

  return (
    <Box as="form" onSubmit={handleSubmit} mt={4}>
      <FormControl id="username" isRequired>
        <FormLabel>Username</FormLabel>
        <Input value={username} onChange={(event) => setUsername(event.target.value)} />
      </FormControl>
      <FormControl id="content" mt={2} isRequired>
        <FormLabel>Comment</FormLabel>
        <Textarea value={content} onChange={(event) => setContent(event.target.value)} />
      </FormControl>
      <Button type="submit" mt={4} colorScheme="blue">Submit</Button>
    </Box>
  );
}

export default CommentForm;
