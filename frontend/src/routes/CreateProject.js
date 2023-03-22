import {
	Input,
	FormControl,
	Text,
	Box,
	VStack,
	Button,
	Flex,
	Checkbox, useBoolean,
	HStack,
	FormErrorMessage,Select
} from '@chakra-ui/react';
import React, { useState } from 'react';
import {createProject, fetchPeople, fetchProjects, getProjectType,getProjectByID, deleteProject, updateProject} from '../api.js';
import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useParams } from 'react-router-dom';


const CreateProject = () => {
	const { 
		id
	 } = useParams();
	const[newName, setNewName] = useState('');
	const[newDescription, setNewDescription] = useState('');
	const [selectedPeople, setSelectedPeople] = useState([]);
	const [selectedProjectType, setselectedProjectType] = useState([]);
	const [projectType, setProjectType] = useState([]);
	const [allPeople, setAllPeople] = useState([]);
	const [projects, setProjects] = useState([]);
	const [formError, setFormError] = useState('');
	const [isPublic,publicToggle] = useBoolean(true);
	const [toggle, set_toggle] = useBoolean();

	let navigate=useNavigate();

	/**
 	* The Function changeDescription creates a new project description.
 	*
 	* @param {string} description - The new description for the project.
 	* @returns {void}
 	*/
	const changeDescription = (description) => {
		setNewDescription(description);
	};

	/**
 	* The Function handleDelete deletes a project with the provided index.
 	*
 	* @returns {void}
 	*/
	const handleDelete = () => {
		deleteProject(id).then((data) => {
			if (data.wasAllowed === false) {
				alert('Project ' + newName + ' is depended upon, can not be deleted.');
			}
			else {
				set_toggle.toggle();
				navigate('../');
			}
		});
	};


	/**
 	* The Function isProjectNameIn checks whether a project with the given name is in the list of projects.
 	*
 	* @param {string} projectName - The name of the project to look for.
 	* @param {Array<Object>} list - The list of projects to search.
 	* @returns {boolean} - True if a project with the given name is found in the list, false otherwise.
 	*/
	const isProjectNameIn = (projectName, list) => {
		let index;
		for (index = 0; index < list.length; index++) {
			if (list[index].projectName === projectName) {
				return true;
			}
		}
		return false;
	};

	/**
 	* Adds a new project to the list of projects.
 	*
 	* @returns {void}
 	*/

	const addProject = () => {
		if (isProjectNameIn(newName, projects)) {
			setFormError('This project name is already used');
		}else{
			createProject({ name: newName, description: newDescription, accounts: selectedPeople }).then(_ => {
				navigate('../');
			});
		}
	};

	/**
 	* The function adjustProjectType adjusts the project type based on the value of the checkbox(private). If private is checked then the user is able to edit people in the project.
 	*
 	* @param {boolean} checked - private
 	* 
 	* @returns {void}
 	*/
	const adjustProjectType = (checked, value) => {
		let list = selectedPeople;
		if (checked){
			list.push(value);
		}
		if(!checked){
			let index = list.indexOf(value);
			list.splice(index,1);
		}
		setProjectType(list);
	};
 

	/**
	* The function adjustSelectedPeople adjusts the list of selected project types.
 	*
 	* @param {boolean} checked
 	*
 	* @returns {void}
 	*/
	const adjustSelectedPeople = (checked, value) => {
		let list = selectedPeople;
		if (checked){
			list.push(value);
		}
		if(!checked){
			let index = list.indexOf(value);
			list.splice(index,1);
		}
		setSelectedPeople(list);
	};

	
	/**
 	* The function below loads the data needed for the projects page.
 	*
 	* @returns {void}
 	*/
	  useEffect(() => {
		if (id){
			async function load_project() {
				let data = await getProjectByID(id);
				console.log(data.data);
				setNewName(data.data.projectName);
				setNewDescription(data.data.projectDescription);
			}
			load_project();
		}else{
			

			async function load_allProjects() {
				let data = await fetchProjects();
				setProjects(data.data);
			
			}
			load_allProjects();

		}
		async function load_allPeople() {
			let data = await fetchPeople();
			setAllPeople(data.data);
		}
		load_allPeople();

	}, []);

	/**
 	* The code below returns a functional component that renders a form for adding or editing a project.
 	*/
	return (<Flex w='100%' minH='80vh' alignItems={'stretch'} p={2} border>
		
		<Box w='100%' minH='100%' bg='white' alignItems='left'>
			
			<VStack p={3} >
				<FormControl isInvalid = {formError !== ''}>

					<Input
						type="text"
						placeholder = {((newName === '')? 'projectName':newName)}
						defaultValue={newName}
						onChange={(event) => setNewName(event.target.value)}
						name="name"
						isDisabled = {id !== undefined}
	
					/>
					<FormErrorMessage>{formError}</FormErrorMessage>
				</FormControl>
				<Input
					type="text"
					placeholder={((newDescription === '')? 'projectDescription':newDescription)}
					defaultValue={newDescription}
					onChange={(event) => changeDescription(event.target.value)}
					name="description"
					isDisabled = {id !== undefined}
				/>
				
				{!id && <Checkbox
					onChange={(e) => publicToggle.toggle()}>
						Private
				</Checkbox>}
			
      			{!isPublic && <>
					<Text>Add People To Project</Text>
					<Box alignItems='left'>
						{allPeople.map((person, index) => {
							return (
								<Checkbox
									key={index}
									onChange={(e) => adjustSelectedPeople(e.target.checked, person.accountID)}>
						    {person.username}
								</Checkbox>
							);
						})}
					</Box>
					<Box alignItems='left'>
						{projectType.map((person, index) => {
							return (
								<Checkbox
									onChange={(e) => adjustProjectType(e.target.checked, person.accountPrivileges)}>
						    {person.accountPrivileges}
								</Checkbox>
							);
						})}
					</Box>
			
				</>
				}
			</VStack>
					
			<HStack>
				{id === undefined && < Button onClick={addProject}>Save Project</Button>}
				{id && (
					<Button 						
						colorScheme='red' 
						variant={'solid'} 
						onClick={() => handleDelete()}>
						Delete Project
					</Button>
				)}
			</HStack>
			
		</Box>		
	</Flex>

	);
};

export default CreateProject;


