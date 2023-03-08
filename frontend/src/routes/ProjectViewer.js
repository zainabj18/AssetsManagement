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
import {createProject, deleteProject, fetchProjects } from '../api.js';
import { useEffect } from 'react';
import {NavLink} from 'react-router-dom';


const ProjectViewer = () => {
	const [projects, setProjects] = useState([]);
	const [toggle, set_toggle] = useBoolean();
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
		<VStack minW="100vw" spacing={3}>
			<VStack>
				{projects && projects.map((projects, index) => {
					return (
						<HStack key={index}>
							<Text> {projects.name} </Text>
							<Text> {projects.description} </Text>
							<IconButton
								left={20}
								icon={<DeleteIcon />}
								colorScheme="blue"
								onClick={() => handleDelete(index)}
							/>
						</HStack>
					);
				})}
			</VStack>
			<NavLink to="./new">Create New Project</NavLink>	
		</VStack>

	);
};

export default ProjectViewer;