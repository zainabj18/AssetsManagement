import {
	Input,
	FormControl,
	FormLabel,
	Text,
	Box,
	VStack,
	Button,
	Flex,
	useBoolean,
	HStack
} from '@chakra-ui/react';
import React, { useState } from 'react';
import { DeleteIcon } from '@chakra-ui/icons';
import { IconButton } from '@chakra-ui/react';
import {deleteProject, fetchProjects, fetchPeopleinProject } from '../api.js';
import { useEffect } from 'react';
//import ProjectPeopleTable from '../components/ProjectPeopleTable.js';
import {NavLink, useParams} from 'react-router-dom';


const ProjectViewer = () => {
	const [projects, setProjects] = useState([]);
	const [toggle, set_toggle] = useBoolean();
	//const [selectedAccounts, setSelectedAccounts]=useState([]);
	const { id } = useParams();

	// const getAccountIDs=()=>{
	// 	return selectedAccounts.map(
	// 		(rowID)=>{return people[rowID].account_id;});
	// };

	useEffect(() => {
		async function load_allProjects() {
			let data = await fetchProjects();
			console.log(data);
			setProjects(data.data);
		}
		load_allProjects();
	}, [toggle]);


	const handleDelete = (index) => {
		const projectToDelete = projects[index];
		console.log('Deleting project with id:', projectToDelete.id);
		deleteProject(projectToDelete.id).then((data) => {
			if (data.wasAllowed === false) {
				alert('Project ' + projectToDelete.name + ' is depended upon, can not be deleted.');
			}
			else {
				set_toggle.toggle();
			}
		});
	};

	return (
		<VStack bg={'whiteAlpha.500'} h={'100%'} w={'100%'} p={2}>
			{projects && projects.map((projects, index) => {
				return (
					<HStack key={index}>
						<Text> {projects.projectName} </Text>
						<Text> {projects.projectDescription} </Text>
						{projects.accounts.map((account, index) => {
							return(
								<Text key = {index}>{account.username}</Text>
							);
						})}
						<IconButton
							left={20}
							icon={<DeleteIcon />}
							colorScheme="blue"
							onClick={() => handleDelete(index)}
						/>
					</HStack>
				);
			})}
			<NavLink to="./new"><Button>Create New Project</Button></NavLink>
			{/* <ProjectPeopleTable people={people} setSelectedAccounts={setSelectedAccounts} />	 */}
		</VStack>
	);
};

export default ProjectViewer;