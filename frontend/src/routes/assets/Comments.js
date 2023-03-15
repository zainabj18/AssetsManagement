import { useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { fetchComments } from '../../api';
import useAuth from '../../hooks/useAuth';
const Comments = () => {

	const { id } = useParams();
	const {user} = useAuth();

	useEffect(() => {
		fetchComments(id).then((data)=>{
			console.log(user.userID);
			console.log(data);
		});
	}, [id,user]);
    
	return (<p>hello</p>);
};
 
export default Comments;