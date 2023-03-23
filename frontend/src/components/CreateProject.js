import {
	Input,
	FormControl,
	Box,
	VStack,
	Button,
	FormErrorMessage, useDisclosure,
	Modal, ModalBody, ModalCloseButton, ModalContent, ModalOverlay, ModalHeader, ModalFooter
} from '@chakra-ui/react';
import React, { useState } from 'react';
import { createProject, fetchProjects } from '../api.js';
import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';


const CreateProject = ({trigger}) => {
	const [newName, setNewName] = useState('');
	const [newDescription, setNewDescription] = useState('');
	const [projects, setProjects] = useState([]);
	const [formError, setFormError] = useState('');
	const { isOpen, onOpen, onClose } = useDisclosure();

	let navigate = useNavigate();

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
		} else {
			createProject({ name: newName, description: newDescription }).then(_ => {
				trigger.toggle();
				onClose();
				navigate('/projects');
			});
		}
	};

	/**
	  * The function below loads the data needed for the projects page.
	  *
	  * @returns {void}
	  */
	useEffect(() => {
		async function load_allProjects() {
			let data = await fetchProjects();
			setProjects(data.data);

		}
		load_allProjects();
	}, []);

	/**
	  * The code below returns a functional component that renders a form for adding or editing a project.
	  */
	return (
		<>
			<Button onClick={onOpen}>New Project</Button>
			<Modal
				closeOnOverlayClick={false}
				isOpen={isOpen}
				onClose={onClose}
				variant="popup"
			>
				<ModalOverlay />
				<ModalContent>
					<ModalHeader>Create New Project</ModalHeader>
					<ModalCloseButton />
					<ModalBody>

						<Box w='100%' minH='100%' bg='white' alignItems='left'>

							<VStack p={3} >
								<FormControl isInvalid={formError !== ''}>

									<Input
										type="text"
										placeholder='Name'
										defaultValue={newName}
										onChange={(event) => setNewName(event.target.value)}
										name="name"

									/>
									<FormErrorMessage>{formError}</FormErrorMessage>
								</FormControl>
								<Input
									type="text"
									placeholder='Description'
									defaultValue={newDescription}
									onChange={(event) => changeDescription(event.target.value)}
									name="description"
								/>
							</VStack>
						</Box>
					</ModalBody>
					<ModalFooter>
						{<Button onClick={addProject}>Save Project</Button>}
					</ModalFooter>
				</ModalContent>
			</Modal >
		</>

	);
};

export default CreateProject;


