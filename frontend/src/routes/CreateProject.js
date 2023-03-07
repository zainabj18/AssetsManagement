import {
	Input,
	FormControl,
	FormLabel,
	Text,
	Box,
	VStack,
	Button,
	Flex,
	Checkbox
} from '@chakra-ui/react';
import React, { useState } from 'react';
import {createProject, fetchPeople, setAllProjects} from '../api.js';
import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';



const CreateProject = () => {
	const[newName, setNewName] = useState('');
	const[newDescription, setNewDescription] = useState('');
	const [toggle] = useEffect();
	let navigate=useNavigate();

	const changeName = (name) => {
		setNewName(name);
	};

	const changeDescription = (description) => {
		setNewDescription(description);
	};

	const addProject = () => {
		createProject({ name: newName, description: newDescription, accountID: selectedPeople }).then(_ => {
			navigate('../');
		});
	};
 
	const [selectedPeople, setSelectedPeople] = useState([]);
	
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
	
	const[allPeople, setAllPeople] = useState([]);
	
	  useEffect(() => {
		async function load_allPeople() {
			let data = await fetchPeople();
			console.log(data);
			setAllProjects(data.data);
		}
		load_allPeople();
	}, [toggle]);


	return (
		<VStack minW="100vw" spacing={3}>
			<Text fontSize='3xl'>Create Project</Text>
			<Box bg='white' w='100%' p={7} color='black'>
				<FormControl isRequired>
					<FormLabel color={'black'}>Project Name</FormLabel>
					<Input
						type="text"
						placeholder="Project Name"

						onChange={(event) => changeName(event.target.value)}
						name="name"
					/>
				</FormControl>
				<FormControl isRequired>
					<FormLabel color={'black'}>Description</FormLabel>
					<Input
						type="text"
						placeholder="Description"
						onChange={(event) => changeDescription(event.target.value)}
						name="description"
					/>
				</FormControl>
			</Box>
			<Flex minWidth='max-content' alignItems='center' gap='4'>
				<Button onClick={addProject}>Save Project</Button>
			</Flex>
			{allPeople.map((person, index) => {
				return (
					<VStack key={person.accountID} align="left">
						<Checkbox>
							onChange={(e) => adjustSelectedPeople(e.target.checked, index)}
						    {person.username}
						</Checkbox>
					</VStack>
				);
			})}
			
		</VStack>

	);
};

export default CreateProject;