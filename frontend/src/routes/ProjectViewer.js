import {
	Text,
	Button,
	useBoolean,
	Table, Thead, Tbody, Tr, Th, Td, TableContainer
} from '@chakra-ui/react';
import React, { useState } from 'react';
import { DeleteIcon } from '@chakra-ui/icons';
import { IconButton } from '@chakra-ui/react';
import {deleteProject, fetchProjects, fetchPeople, deletePeople} from '../api.js';
import { useEffect } from 'react';
import {NavLink} from 'react-router-dom';



const ProjectViewer = () => {
	const [projects, setProjects] = useState([]);
	const [accounts, setAccounts] = useState([]);
	const [toggle, set_toggle] = useBoolean();

	useEffect(() => {
		async function load_allPeople() {
			let data = await fetchPeople();
			console.log(data);
			setAccounts(data.data);
		}
		load_allPeople();

		async function load_allProjects() {
			let data = await fetchProjects();
			console.log(data);
			setProjects(data.data);
			
		}
		load_allProjects();
	}, [toggle]);


	const handleDelete = (index) => {
		const DeleteProjectAndPeople = projects[index];
		console.log('Deleting project:', DeleteProjectAndPeople);
		deleteProject(DeleteProjectAndPeople.projectID).then((data) => {
			if (data.wasAllowed === false) {
				alert('Project ' + DeleteProjectAndPeople.projectName + ' is depended upon, can not be deleted.');
			}
			else {
				set_toggle.toggle();
			}
		});
	};

	const handleDeletePeople = (index) => {
		const DeletePeople = accounts[index];
		console.log('Deleting people:', DeletePeople.accountID);
		deletePeople(DeletePeople.accountID).then((data) => {
			if (data.wasAllowed === false) {
				alert('People ' + DeletePeople.username + ' is depended upon, can not be deleted.');
			}
			else {
				set_toggle.toggle();
			}
		});
	};

	return (
		<div>
			<TableContainer>
				<Table variant='simple'>
					<Thead>
						<Tr>
							<Th color='Black'>Name</Th>
							<Th color='Black'>Description</Th>
							<Th color='Black'>Accounts</Th>
							<Th color='Black'>Delete project</Th>
							<Th color='Black'>Delete people</Th>
						</Tr>
					</Thead>
					<Tbody>			
						{projects && projects.map((projects, index) => {
							return (
								<Tr key={index}>
									<Td>{projects.projectName} </Td>
									<Td>{projects.projectDescription} </Td>
									<Td>{projects.accounts.map((account, index) => {
										return(
											<Text key = {index}>{account.username}</Text>
										);
									})}</Td>
									<Td><Button
										left={0.9}
										colorScheme='red' 
										variant={'solid'}
										onClick={() => handleDelete(index)}
									>Delete project</Button>
									</Td>
									<Td>
										{projects.accounts.map((index) => {
											return (
												<Button
													left={0.9}
													colorScheme='blue' 
													onClick={() => handleDeletePeople(index)}
												>Delete account</Button>
											);
										})}
									</Td>
								</Tr>
							);
						})}
					</Tbody>
				</Table>
			</TableContainer>
			<NavLink to="./new"><Button>Create New Project</Button></NavLink>
		</div>
	);
	
};

export default ProjectViewer;