import { Box, Button, Center, FormControl, FormLabel, HStack, Heading, Input, Select, Stack, InputGroup, InputRightElement, Alert, AlertIcon, AlertTitle, AlertDescription } from '@chakra-ui/react';
import { React, useEffect, useState } from 'react';
import useAuth from '../hooks/useAuth';
import { createUser, deleteUserAcc } from '../api';

const User = () => {
	const { user } = useAuth();

	useEffect(() => {
		console.log(user);
	}, []);

	const [inputFields, setInputFields] = useState([{first_name: '', last_name: '', username: '', password: '', confirmPassword: '', account_privileges: '', account_type: '' }]);
	const [deleteuser, setDeleteUser] = useState([{delete: ''}]);
	const [saveuser, setSaveUser] = useState([{save: ''}]);
	const [accountPrivileges, setAccountPrivileges] = useState([]);
	const [accountTypes, setAccountTypes] = useState([]);
	const [show, setShow] = useState(false);
	const { authError } = useAuth();
	const [error, setError] = useState(null);
	const [success, setSuccess] = useState(false);

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
		  	return field.first_name !== '' && field.last_name !== '' && field.username !== '' && field.password !== '' && field.confirmPassword !== '';
		});
	  
		if (isFormValid) {
			const userData = {
				first_name: inputFields[0].first_name,
				last_name: inputFields[0].last_name,
				username: inputFields[0].username,
				password: inputFields[0].password,
				confirmPassword: inputFields[0].confirmPassword,
				account_privileges: inputFields[0].account_privileges,
				account_type: inputFields[0].account_type
			};
	  
			try {
				const response = await createUser(userData);
				console.log(response.data);
				setSuccess(true);
				setError(false);
				
			} catch (error) {
				setSuccess(false);
				if (error.response.status === 400) {
					setError({ error: error.response.data.error, msg: error.response.data.msg });
				} else {
					console.error(error);
				}
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
							<Input type='text' placeholder="Name" defaultValue={attr.first_name} onChange={event => handleFormChange(index, event)} name="first_name"/>
						</FormControl>
						<FormControl>
							<FormLabel>Last Name</FormLabel>
							<Input type='text' placeholder="Surname" defaultValue={attr.last_name} onChange={event => handleFormChange(index, event)} name="last_name"/>
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

				{inputFields.map((attr, index) => {return (
					<HStack spacing={'25px'} mt={'25px'} key={index}>
						<FormControl>
							<FormLabel>Access Level</FormLabel>
							<Select placeholder='Select Access Level' color='black' bg='white' defaultValue={attr.account_privileges} onChange={event => handleFormChange(index, event)} name = 'account_privileges'>
								<option value='PUBLIC'>PUBLIC</option>
								<option value='INTERNAL'>INTERNAL</option>
								<option value='RESTRICTED'>RESTRICTED</option>
								<option value='CONFIDENTIAL'>CONFIDENTIAL</option>
							</Select>
						</FormControl>
						<FormControl>
							<FormLabel>Role</FormLabel>
							<Select placeholder='Select Role' color='black' bg='white' defaultValue={attr.account_type} onChange={event => handleFormChange(index, event)} name = 'account_type'>
								<option value='VIEWER'>VIEWER</option>
								<option value='USER'>USER</option>
								<option value='ADMIN'>ADMIN</option>
							</Select>
						</FormControl>
					</HStack>
				);})}

				{error && (<Alert status='error'>
  							<AlertIcon />
					<AlertTitle>{error.error}</AlertTitle>
					<AlertDescription>{error.msg}</AlertDescription>
				</Alert>)}

				{success && (<Alert status="success">
					<AlertIcon />
					<AlertTitle>Registration successful.</AlertTitle>
					<AlertDescription>User has been registered.</AlertDescription>
				</Alert>)}

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


