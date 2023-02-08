import {
	Input,
	FormControl,
	FormLabel,
	Text,
	VStack,
	Button,
} from '@chakra-ui/react';
//import axios from 'axios';
import React, { useState } from 'react';
import { DeleteIcon } from '@chakra-ui/icons';
import { IconButton } from '@chakra-ui/react';
import {createProject} from '../api.js';
const CreateProject = () => {
	const [projects, setProjects] = useState([{ name: '', description: '' }]);

	const handleCreate = (index, event) => {
		let data = [...projects];
		data[index][event.target.name] = event.target.value;
		setProjects(data);
	};

	const addProject = () => {
		setProjects([...projects, { name: '', description: '' }]);
	};
	const submitProject = () => {
		console.log(projects);
		projects.forEach((val, i) => createProject(val));
		
	};

	const deleteProject = (index) => {
		let data = [...projects];
		data.splice(index, 1);
		setProjects(data);
	};

	return (
		<VStack minW="100vw">
			<Text>Create Project</Text>
			{projects.map((project, index) => {
				return (
					<VStack key={index}>
						<FormControl isRequired>
							<FormLabel>Project Name</FormLabel>
							<Input
								type="text"
								placeholder="Project Name"
								defaultValue={project.name}
								onChange={(event) => handleCreate(index, event)}
								name="name"
							/>
						</FormControl>
						<FormControl isRequired>
							<FormLabel>Description</FormLabel>
							<Input
								type="text"
								placeholder="Description"
								defaultValue={project.description}
								onChange={(event) => handleCreate(index, event)}
								name="description"
							/>
						</FormControl>
						<IconButton
							icon={<DeleteIcon />}
							colorScheme="blue"
							onClick={() => deleteProject(index)}
						/>
					</VStack>
				);
			})}
			<Button onClick={addProject}>Add Project</Button>
			<Button onClick={submitProject}> Submit</Button>
		</VStack>
	);
};

export default CreateProject;
