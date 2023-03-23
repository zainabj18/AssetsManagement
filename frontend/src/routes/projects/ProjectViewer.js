import { Button, ButtonGroup, Heading, Text, useBoolean, VStack } from '@chakra-ui/react';
import { useEffect, useState } from 'react';
import { useNavigate, useParams, useOutletContext } from 'react-router-dom';
import { deleteProject, fetchAssetsinProject} from '../../api';
import AssetTable from '../../components/assets/AssetTable';
import useAuth from '../../hooks/useAuth';

const ProjectViewer = () => {
	const { user } = useAuth();
	const [assetsin, setAssets] = useState([]);
	const [selectedAssets, setSelectedAssets] = useState([]);
	const [project, setProject] = useState('');
	const [trigger, setTrigger] = useBoolean();
	const { id } = useParams();
	const [update, setUpdate] = useOutletContext();

	let navigate = useNavigate();

	const handleDelete = () => {
		if (assetsin.length <= 0) {
			deleteProject(id).then(_ => {
				setTrigger.toggle();
				setUpdate.toggle();
				navigate('/projects');
			});
		}
		else {
			alert('Project has assets linked. Can not delete: ' + project.name + '.');
		}
	};

	useEffect(() => {
		fetchAssetsinProject(id).then((res) => {
			console.log(res.data);
			setAssets(res.data.assets);
			setProject(res.data.project);
		});
		;
	}, [id, trigger, user]);

	return (<VStack bg={'whiteAlpha.500'} h={'100%'} w={'100%'} p={2}>
		<Heading>{project.name}</Heading>
		<Text>{project.description}</Text>
		<AssetTable assets={assetsin} setSelectedAssets={setSelectedAssets} preSelIDs={[]} />
		{(user && user.userRole !== 'VIEWER') &&
			<ButtonGroup>
				{user.userRole === 'ADMIN' &&
					<Button colorScheme='red' variant={'solid'} onClick={handleDelete}>Delete Project</Button>}
			</ButtonGroup>}
	</VStack>);
};

export default ProjectViewer;