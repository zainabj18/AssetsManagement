import {
	Input,
	FormControl,
	FormLabel,
	Text,
	Box,
	VStack,
	Button,
	Flex,
	useBoolean
} from '@chakra-ui/react';
//import axios from 'axios';
import React, { useState } from 'react';
import { DeleteIcon } from '@chakra-ui/icons';
import { IconButton } from '@chakra-ui/react';
import {createProject, deleteProject, fetchAllProjects } from '../api';
import { useEffect} from 'react';

const CreateProject = () => {
	const [projects, setProjects] = useState([{ name: '', description: '' }]);
	const [toggle, set_toggle] = useBoolean();

	useEffect(() => {
		async function load_allProjects() {
			let data = await fetchAllProjects(res => res.data);
			setProjects(data);
		}
		load_allProjects();
	}, [toggle]);

	
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

	const handleDelete = (index) => {
		const projectToDelete = projects[index];
		deleteProject(projectToDelete.id).then((data) => {
			if (data.wasAllowed == false) {
				alert('Project ' + projects.name + ' is depended upon, can not be deleted.');
			}
			else {
				//setProjects((prevProjects) => prevProjects.filter((p, i) => i !== index));
				set_toggle.toggle();
			}
		});
	};

	return (
		<VStack minW="100vw" spacing={3}>
			<Text fontSize='3xl'>Create Project</Text>
  
			{projects.map((project, index) => {
				return (
					<VStack key={index}>
						<Box bg='white' w='100%' p={7} color='black'>
							<FormControl isRequired>
								<FormLabel color={'black'}>Project Name</FormLabel>
								<Input
									type="text"
									placeholder="Project Name"
									defaultValue={project.name}
									onChange={(event) => handleCreate(index, event)}
									name="name"
								/>
							</FormControl>
							<FormControl isRequired>
								<FormLabel color={'black'}>Description</FormLabel>
								<Input
									type="text"
									placeholder="Description"
									defaultValue={project.description}
									onChange={(event) => handleCreate(index, event)}
									name="description"
								/>
							</FormControl>
							
							<IconButton
								left={20}
								icon={<DeleteIcon />}
								colorScheme="blue"
								onClick={() => handleDelete(index)}
							/>
						</Box>
					</VStack>
				);
			})}
			<Flex minWidth='max-content' alignItems='center' gap='4'>
				<Button onClick={addProject}>Add Project</Button>
				<Button onClick={submitProject}> Submit</Button>
			</Flex>
			
		</VStack>

	);
};

export default CreateProject;
