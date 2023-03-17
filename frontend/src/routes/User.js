import { Box, Button, Center, FormControl, FormLabel, HStack, Heading, Input, Select, Stack, InputGroup, InputRightElement } from '@chakra-ui/react';
import { React, useEffect, useState } from 'react';
import useAuth from '../hooks/useAuth';
import { createUser, deleteUserAcc } from '../api';

const User = () => {
	const { user } = useAuth();

	useEffect(() => {
		console.log(user);
	}, []);

	const [inputFields, setInputFields] = useState([{name: '', surname: '', username: '', password: '', confirmPassword: '' }]);
	const [deleteuser, setDeleteUser] = useState([{delete: ''}]);
	const [saveuser, setSaveUser] = useState([{save: ''}]);
	const [accountPrivileges, setAccountPrivileges] = useState([]);
	const [accountTypes, setAccountTypes] = useState([]);
	const [show, setShow] = useState(false);

	const handleClick = () => setShow(!show);

	const handleFormChange = (index, event) => {
		let data = [...inputFields];
		data[index][event.target.name] = event.target.value;
		setInputFields(data);
	};

	const deleteUser = async (index) => {
		const userIdToDelete = inputFields[index].id;
		try {
		  await deleteUserAcc(userIdToDelete);
		  let data = [...deleteuser];
		  data.splice(index, 1);
		  setDeleteUser(data);
		} catch (error) {
		  console.error(error);
		}
	  };

	const saveUser = async (e) => {
		e.preventDefault();
	  
		const isFormValid = inputFields.every((field) => {
		  	return field.name !== '' && field.surname !== '' && field.username !== '' && field.password !== '' && field.confirmPassword !== '';
		});
	  
		if (isFormValid) {
			const userData = {
				name: inputFields[0].name,
				surname: inputFields[0].surname,
				username: inputFields[0].username,
				password: inputFields[0].password,
				confirmPassword: inputFields[0].confirmPassword,
				account_privileges: inputFields[0].account_privileges,
				account_type: inputFields[0].account_type
			};
	  
			try {
				const response = await createUser(userData);
				console.log(response.data);
			} catch (error) {
				console.error(error);
			}
		}
	};

	return (
		<Center height={'90vh'}>
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
				
				{inputFields.map((attr, index) => {return (
					<HStack spacing={'25px'} mt={'25px'} key={index}>
						<FormControl>
							<FormLabel>Password</FormLabel>
							<InputGroup>
								<Input type={show ? 'text' : 'password'} placeholder="Password" defaultValue={attr.password} onChange={event => handleFormChange(index, event)} name="password"/>
								<InputRightElement width='4.5rem'>
									<Button h='1.75rem' size='sm' onClick={handleClick}>
										{show ? 'Hide' : 'Show'}
									</Button>
								</InputRightElement>
							</InputGroup>
						</FormControl>
						<FormControl>
							<FormLabel>Confirm Password</FormLabel>
							<InputGroup>
								<Input type={show ? 'text' : 'password'} placeholder="Confirm Password" defaultValue={attr.confirmPassword} onChange={event => handleFormChange(index, event)} name="confirmPassword"/>
								<InputRightElement width='4.5rem'>
									<Button h='1.75rem' size='sm' onClick={handleClick}>
										{show ? 'Hide' : 'Show'}
									</Button>
								</InputRightElement>
							</InputGroup>
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
						<Button colorScheme='red' variant='solid' size='md' onClick={deleteUser}>
				Delete
						</Button>
					</Stack>
				);})}
			</Box>
		</Center>
	);
};

export default User;


