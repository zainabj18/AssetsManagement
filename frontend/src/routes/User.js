import { Box, Button, Center, FormControl, FormLabel, HStack, Heading, Input, Select, Stack } from '@chakra-ui/react';
import { React, useEffect, useState } from 'react';
import useAuth from '../hooks/useAuth';

const User = () => {
	const { user } = useAuth();

	useEffect(() => {
		console.log(user);
	});

	const [textInput, setTextInput] = useState([{name: '', surname: '', username: '' }]);
	const [deleteobject, setDeleteObject] = useState([{delete: ''}]);
	const [saveobject] = useState([{save: ''}]);

	return (
		<Center height={'100vh'}>
			<Box bg={'white'} color={'black'} p={10} borderRadius={10} w={'1000px'} mx={'auto'} mb={'100px'}>
				<Heading mb={'25px'}>Your Profile</Heading>
				<HStack spacing={'25px'}>
					<FormControl>
						<FormLabel>First Name</FormLabel>
						<Input type='text' placeholder="Name" />
					</FormControl>
					<FormControl>
						<FormLabel>Last Name</FormLabel>
						<Input type='text' placeholder="Surname" />
					</FormControl>
					<FormControl>
						<FormLabel>Username</FormLabel>
						<Input type='text' placeholder="Username" />
					</FormControl>
				</HStack>

				<HStack spacing={'25px'} mt={'25px'}>
					<FormControl>
						<FormLabel>Access Level</FormLabel>
						<Select placeholder='Select Access Level' color='black' bg='white'>
							<option value='option1'>Option 1</option>
							<option value='option2'>Option 2</option>
							<option value='option3'>Option 3</option>
						</Select>
					</FormControl>
					<FormControl>
						<FormLabel>Role</FormLabel>
						<Select placeholder='Select Role' color='black' bg='white'>
							<option value='option1'>Option 1</option>
							<option value='option2'>Option 2</option>
							<option value='option3'>Option 3</option>
						</Select>
					</FormControl>
				</HStack>

				<Stack direction='row' align='center' mt={8}>
					<Button colorScheme='blue' variant='solid' size='md'>
              Save
					</Button>
					<Button colorScheme='red' variant='solid' size='md'>
              Delete
					</Button>
				</Stack>
			</Box>
		</Center>
	);
};

export default User;

