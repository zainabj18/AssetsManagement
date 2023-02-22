import {
	Input,
	FormControl,
	FormLabel,
	Text,
	Box,
	VStack,
	Button,
	Flex
} from '@chakra-ui/react';
import React, { useState } from 'react';
import {createProject} from '../api.js';
import { useNavigate } from 'react-router-dom';



const CreateProject = () => {
	const[newName, setNewName] = useState('');
	const[newDescription, setNewDescription] = useState('');
	let navigate=useNavigate();

	const changeName = (name) => {
		setNewName(name);
	};

	const changeDescription = (description) => {
		setNewDescription(description);
	};

	const addProject = () => {
		createProject({ name: newName, description: newDescription }).then(_ => {
			navigate('../');
		});
	};

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
			
		</VStack>

	);
};

export default CreateProject;

