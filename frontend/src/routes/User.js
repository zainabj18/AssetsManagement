import { Box, Button, Center, FormControl, FormLabel, HStack, Heading, Input, Select, Stack } from '@chakra-ui/react';
import { React, useEffect, useState } from 'react';
import useAuth from '../hooks/useAuth';

const User = () => {
	const { user } = useAuth();

	useEffect(() => {
		console.log(user);
	});

	const [inputFields, setInputFields] = useState([{name: '', surname: '', username: '' }]);
	const [deleteobject, setDeleteObject] = useState([{delete: ''}]);
	const [saveobject] = useState([{save: ''}]);

	const handleFormChange = (index, event) => {
		let data = [...inputFields];
		data[index][event.target.name] = event.target.value;
		setInputFields(data);
	};

	const deleteObject = (index) => {
		let data = [...deleteobject];
		data.splice(index, 1);
		setDeleteObject(data);
	};

	const saveUser = (e) => {
		e.preventDefault();
		console.log(saveobject);
	};

	return (
		<Center height={'100vh'}>
			<Box bg={'white'} color={'black'} p={10} borderRadius={10} w={'1000px'} mx={'auto'} mb={'100px'}>
				<Heading mb={'25px'}>Your Profile</Heading>
				{inputFields.map((attr, index) => {return (
					<HStack spacing={'25px'} key={index}>
						<FormControl>
							<FormLabel>First Name</FormLabel>
							<Input type='text' placeholder="Name" defaultValue={attr.name} onChange={event => handleFormChange(index, event)} name="name"/>
						</FormControl>
						<FormControl>
							<FormLabel>Last Name</FormLabel>
							<Input type='text' placeholder="Surname" defaultValue={attr.surname} onChange={event => handleFormChange(index, event)} name="surname"/>
						</FormControl>
						<FormControl>
							<FormLabel>Username</FormLabel>
							<Input type='text' placeholder="Username" defaultValue={attr.username} onChange={event => handleFormChange(index, event)} name="username"/>
						</FormControl>
					</HStack>
				);})}

				{inputFields.map((user) => {return (
					<HStack spacing={'25px'} mt={'25px'} key={user.account_id}>
						<FormControl>
							<FormLabel>Access Level</FormLabel>
							<Select placeholder='Select Access Level' color='black' bg='white'>
								<option value='option1'>{user.account_privileges}</option>
							</Select>
						</FormControl>
						<FormControl>
							<FormLabel>Role</FormLabel>
							<Select placeholder='Select Role' color='black' bg='white'>
								<option value='option1'>{user.account_type}</option>
							</Select>
						</FormControl>
					</HStack>
				);})}

				{inputFields.map((index) => {return (
					<Stack direction='row' align='center' mt={8}>
						<Button colorScheme='blue' variant='solid' size='md' onClick={saveUser}>
				Save
						</Button>
						<Button colorScheme='red' variant='solid' size='md' onClick={deleteObject}>
				Delete
						</Button>
					</Stack>
				);})}
			</Box>
		</Center>
	);
};

export default User;


