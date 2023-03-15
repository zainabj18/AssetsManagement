import { Box, VStack,Text, Flex, StackDivider, HStack } from '@chakra-ui/react';
import { useEffect, useRef, useState } from 'react';
import { Link, NavLink, useParams } from 'react-router-dom';
import { fetchComments } from '../../api';
import useAuth from '../../hooks/useAuth';
import {TimeIcon} from '@chakra-ui/icons';

const ScrollToBottom = () => {
	const endRef = useRef();
	useEffect(() => endRef.current.scrollIntoView({ behavior: 'smooth' }));
	return <div ref={endRef} />;
};
const Comments = () => {
	const [comments, setComments] = useState([]);
	const { id } = useParams();
	const {user} = useAuth();

	useEffect(() => {

		fetchComments(id).then((res)=>{
			console.log(user.userID);
			console.log(res.data);
			setComments(res.data);

		});
	}, [id,user]);
    
	return (
		<VStack display="flex" flexDirection='column' bg="tomato" spacing={4} padding={4} overflowY='scroll' maxH="70vh">
			{comments.map((comment, index) => {return (
				<Box 
					key={index}
					backgroundColor="white"
					borderRadius='md' 
					padding={2}
					maxWidth="80%"
					alignSelf={index >1?'flex-start':'flex-end'}>
					<Link to={`/profile/${comment.accountID}`} as={NavLink}><Text as='b'>{comment.username}</Text></Link>

					<Text>{comment.comment}</Text>
					<HStack>
						<TimeIcon/>
						<Text as="i" fontSize='xs'>{new Date(comment.datetime).toLocaleString()}</Text>
					</HStack>
			  	</Box>	
			);})}
			<ScrollToBottom />
	  </VStack>
	);
	
};
 
export default Comments;