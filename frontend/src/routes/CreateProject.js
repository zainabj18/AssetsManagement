import {
	Input,
	FormControl,
	FormLabel,
	Text,
	Box,
	VStack,
	Button,
	Flex,
	Checkbox, useBoolean,
	HStack,
	FormErrorMessage
} from '@chakra-ui/react';
import React, { useState } from 'react';
import {createProject, fetchPeople, fetchProjects} from '../api.js';
import NewTag from '../components/NewTag';
import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Outlet } from 'react-router-dom';



const CreateProject = () => {
	const[newName, setNewName] = useState('');
	const[newDescription, setNewDescription] = useState('');
	const [toggle, set_toggle] = useBoolean();
	const [selectedPeople, setSelectedPeople] = useState([]);
	const [allPeople, setAllPeople] = useState([]);
	const [projects, setProjects] = useState([]);
	const [formError, setFormError] = useState('');

	let navigate=useNavigate();


	const changeDescription = (description) => {
		setNewDescription(description);
	};

	//projectName

	const isProjectNameIn = (projectName, list) => {
		let index;
		for (index = 0; index < list.length; index++) {
			if (list[index].projectName === projectName) {
				return true;
			}
		}
		return false;
	};

	const addProject = () => {
		console.log(newName);
		console.log(projects);
		if (isProjectNameIn(newName, projects)) {
			setFormError('This project name is already used');
		}else{
			createProject({ name: newName, description: newDescription, accounts: selectedPeople }).then(_ => {
				navigate('../');
			});
		}

	};
 

	
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
	
	
	  useEffect(() => {
		async function load_allPeople() {
			let data = await fetchPeople();
			console.log(data);
			setAllPeople(data.data);
		}
		load_allPeople();

		async function load_allProjects() {
			let data = await fetchProjects();
			setProjects(data.data);
			
		}
		load_allProjects();
	}, [toggle]);


	return (<Flex w='100%' minH='80vh' alignItems={'stretch'} p={2} border>
		{/* <Text fontSize='3xl'>Create Project</Text> */}
		<Box w='30%' minH='100%' bg='gray.300' p={4} color='black' align={'top'}>
			<FormControl isInvalid = {formError !== ''}>
				<Input
					type="text"
					placeholder="Project Name"

					onChange={(event) => setNewName(event.target.value)}
					name="name"
				/>
				<FormErrorMessage>{formError}</FormErrorMessage>
			</FormControl>
			<HStack>
				<Input
					type="text"
					placeholder="Description"
					onChange={(event) => changeDescription(event.target.value)}
					name="description"
				/>
			</HStack>
		</Box>
		<VStack p={2}>
			{allPeople.map((person, index) => {
				return (
					<VStack key={person.accountID} align="left">
						<Checkbox
							onChange={(e) => adjustSelectedPeople(e.target.checked, person.accountID)}>
						    {person.username}
						</Checkbox>
					</VStack>
				);
			})}
		</VStack>
		<HStack>
			<Button onClick={addProject}>Save Project</Button>
		</HStack>
		<Box w='70%' minH='100%' bg='white' alignItems='center'>
			<Outlet/>
		</Box>		
	</Flex>

	);
};

export default CreateProject;

