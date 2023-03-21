import {
	Text,
	Button,
	useBoolean,
	Table, Thead, Tbody, Tr, Th, Td, TableContainer
} from '@chakra-ui/react';
import React, { useState } from 'react';
import {deleteProject, fetchProjects, fetchPeople, deletePeople, projectType} from '../api.js';
import { useEffect } from 'react';
import {NavLink} from 'react-router-dom';



const ProjectViewer = () => {
	const [projects, setProjects] = useState([]);
	const [accounts, setAccounts] = useState([]);
	const [toggle, set_toggle] = useBoolean();

	/**
	 * Runs two functions to load people and projects data from a server.
	 * The loaded data is stored in the state variables accounts and projects respectively.
	 * The useEffect hook runs every time the 'toggle' variable changes.
	 * @function
	 * @name useEffect
	 * @param {function} function A function that loads all the people and project data from the server.
	 * @param {array} [toggle] An array of dependencies that the effect depends on. The effect only runs when any of the dependencies change.
	 */
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



	/**
	 * Deletes a project and its associated people.
	 * @param {number} index - The index of the project to be deleted in the projects array.
	*/
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

	/**
	 * Handles the deletion of a person from the project.
	 * @param {number} index - The index of the person to be deleted.
	 * @returns {void}
	*/
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

	/**
	 * Returns a table with projects' names, descriptions, and associated accounts' usernames and privileges,
	 * as well as buttons to delete projects and associated accounts, and a button to create a new project.
	*/
	return (
		<div>
			<TableContainer>
				<Table variant='simple'>
					<Thead>
						<Tr>
							<Th color='Black'>Name</Th>
							<Th color='Black'>Description</Th>
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
									<Td>{projects.accounts.map((account, index) => {
										return(
											<Text key = {index}>{account.account_privileges}</Text>
										);
									})}</Td>
									<Td><Button
										left={0}
										colorScheme='red' 
										variant={'solid'}
										onClick={() => handleDelete(index)}
									>Delete project</Button>
									</Td>
									<Td>
										{projects.accounts.map((accounts, index) => {
											return (
												<Button
													left={0.9}
													colorScheme='blue' 
													onClick={() => handleDeletePeople(index)}
												>Delete people</Button>

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