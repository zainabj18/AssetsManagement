import { Button} from '@chakra-ui/react';
import axios from 'axios';
const CreateProject = () => {
	const handleCreate = () => {
		axios.post('/api/v1/projects/new',{}).then((res) => {
			console.log(res);
		}
		).catch( (res) =>{
			console.log(res);
		});};
	return <div><Button onClick={handleCreate}>Create</Button></div>;
};

export default CreateProject;