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
	HStack
} from '@chakra-ui/react';
import React, { useState } from 'react';
import {createProject, fetchPeople} from '../api.js';
import NewTag from '../components/NewTag';
import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Outlet } from 'react-router-dom';



const CreateProject = () => {
	const[newName, setNewName] = useState('');
	const[newDescription, setNewDescription] = useState('');
	const [toggle, set_toggle] = useBoolean();
	const [trigger,setTrigger]=useBoolean();

	let navigate=useNavigate();

	const changeName = (name) => {
		setNewName(name);
	};

	const changeDescription = (description) => {
		setNewDescription(description);
	};

	const addProject = () => {
		createProject({ name: newName, description: newDescription, accounts: selectedPeople }).then(_ => {
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
			setAllPeople(data.data);
		}
		load_allPeople();
	}, [toggle]);


	return (<Flex w='100%' minH='80vh' alignItems={'stretch'} p={2} border>
		{/* <Text fontSize='3xl'>Create Project</Text> */}
		<Box w='30%' minH='100%' bg='gray.300' p={4} color='black' align={'top'}>
			<HStack>
				<Input
					type="text"
					placeholder="Project Name"

					onChange={(event) => changeName(event.target.value)}
					name="name"
				/>
				<NewTag trigger={setTrigger}/>
			</HStack>
			<HStack>
				<Input
					type="text"
					placeholder="Description"
					onChange={(event) => changeDescription(event.target.value)}
					name="description"
				/>
				<NewTag trigger={setTrigger}/>
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




	
	// 	return (
	// 		<Flex w='100%' minH='80vh' alignItems={'stretch'} p={2} border>
	// 			<Box w='30%' minH='100%' bg='gray.300' p={4} color='black' align={'top'}>
	// 				<HStack>
	// 					<Input type='text' placeholder='Search for tag ...' onChange={(e)=>{filter(e.target.value);}}/>
	// 					<NewTag trigger={setTrigger}/>
	// 				</HStack>
	// 				<VStack p={2}>
	// 					{results.map((t,index)=>(
	// 						<CustomNavLink key={index} to={`./${t.id}`} w='100%'>
	// 							{t.name}
	// 						</CustomNavLink>

	// 					))}
				
// 				</VStack>
// 			</Box>
// 			<Box w='70%' minH='100%' bg='white'>
// 				<Outlet />
// 			</Box> 
// 		</Flex>
// 	);
};

export default CreateProject;
