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
	HStack,
	Table, Thead, Tbody, Tr, Th, Td, TableContainer, TableCaption
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
	<div style={{borderColor:"#fff"}}>
			<Box background="white"  overflow={"scroll"} height={'72vh'} boxShadow="0 3px 6px #00000029" width={'60vw'} p={0} m={0} rounded="2xl" borderColor={'white'}  >
				<Table variant='simple'  bg="white"  >
					<Thead>
						<Tr>
							<Th color='Black'>Name</Th>
							<Th color='Black'>Description</Th>
							<Th color='Black'>Accounts</Th>
							<Th color='Black'>Delete</Th>
						</Tr>
					</Thead>
					<Tbody>			
						{projects && projects.map((projects, index) => {
							return (
								<Tr key={index} sx={{border:'none',
								'&:nth-of-type(odd)': {
									td:{
										bg:'white',
										color:'blue.900'
									}
								},
								'&:nth-of-type(even)': {
									td: {
										bg:'blue.100',
										color:'blue.900'
									}}}}>
									<Td>{projects.projectName} </Td>
									<Td>{projects.projectDescription} </Td>
									<Td>{projects.accounts.map((account, index) => {
										return(
											<Text key = {index}>{account.username}</Text>
										);
									})}</Td>
									<Td><IconButton
										icon={<DeleteIcon />}
										colorScheme="blue"
										onClick={() => handleDelete(index)}
									/>
									</Td>
								</Tr>
							);
						})}
					</Tbody>
				</Table>
			</Box>
			<NavLink to="./new" ><Button marginY={5}>Create New Project</Button></NavLink>
		</div>
	);
	
};

export default ProjectViewer;