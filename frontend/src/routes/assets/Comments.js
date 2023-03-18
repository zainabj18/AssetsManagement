import { Box, VStack,Text, Flex, StackDivider, HStack, Input, Button, Textarea,IconButton,useToast, Alert, AlertTitle, useBoolean, Spacer } from '@chakra-ui/react';
import { useEffect, useRef, useState } from 'react';
import { Link, NavLink, useParams } from 'react-router-dom';
import { fetchComments,addComment, deleteComment } from '../../api';
import useAuth from '../../hooks/useAuth';
import {TimeIcon,DeleteIcon} from '@chakra-ui/icons';
import { MdMessage } from 'react-icons/md';

const ScrollToBottom = () => {
	const endRef = useRef();
	useEffect(() => endRef.current.scrollIntoView({ behavior: 'smooth' }));
	return <div ref={endRef} />;
};
const Comments = () => {
	const { id } = useParams();
	const {user} = useAuth();
	const toast = useToast();
	const [comments, setComments] = useState([]);
	const [newComment, setNewComment] = useState('');
	const [toggle, setToggle] = useBoolean();
	const handleCommentChange = (e) => {
		let input = e.target.value;
		setNewComment(input);
	};

	const addNewComment=()=>{
		addComment(id,{comment:newComment}).then(res=>{
			setToggle.toggle();
			setNewComment('');
		}
		);
	};
	const removeComment=(comment_id)=>{
		deleteComment(id,comment_id).then(res=>{
			setToggle.toggle();
		}
		);
	};

	useEffect(() => {

		fetchComments(id).then((res)=>{
			console.log(user.userID);
			console.log(res.data);
			setComments(res.data);

		});
	}, [id,user,toggle]);
    
	return (
		<Box>
			<VStack display="flex" flexDirection='column' bg="tomato" spacing={4} padding={4} overflowY='scroll' maxH="70vh">
				<Text as="em">This is the start of the dicussion</Text>
				{comments.map((comment, index) => {return (
					<Box 
						key={index}
						backgroundColor="white"
						borderRadius='md' 
						padding={2}
						maxWidth="80%"
						alignSelf={comment.accountID===user.userID?'flex-end':'flex-start'}>
						<Flex>
							<Link to={`/profile/${comment.accountID}`} as={NavLink}><Text as='b'>{comment.username}</Text></Link>
							<Spacer />

							{user.userRole==='ADMIN' && <IconButton icon={<DeleteIcon />} boxSize={6} bg="red" onClick={()=>removeComment(comment.comment_id)}/>}
						</Flex>
						

						<Text>{comment.comment}</Text>
						<HStack>
							<TimeIcon/>
							<Text as="i" fontSize='xs'>{new Date(comment.datetime).toLocaleString()}</Text>
						</HStack>
			  	</Box>	
				);})}
				<ScrollToBottom />
			
			
	  </VStack>
	  {user.userRole!=='VIEWER' && (<HStack minW={'100%'} bg="gray.700" padding={4} align='center'>
	  <Textarea resize="none" bg="gray.300" placeholder='New Comment'
	  value={newComment}
	  onChange={handleCommentChange}/>
	  {newComment.length>0 && <IconButton icon={<MdMessage />} minH={'100%'} onClick={addNewComment}/>}
			</HStack>)}
	  
		</Box>

	);
	
};
 
export default Comments;