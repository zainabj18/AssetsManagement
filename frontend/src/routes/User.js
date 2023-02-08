import { FormControl, FormLabel, HStack, Input} from '@chakra-ui/react';
import { Box } from '@chakra-ui/react';
import { React, useEffect, useState } from 'react';
import { Flex, InputGroup, InputLeftAddon } from '@chakra-ui/react';
import { Select } from '@chakra-ui/react';
import { Stack, Button} from '@chakra-ui/react';
import useAuth from '../hooks/useAuth';
const User = () => {
	const { user } = useAuth();

	useEffect(() => {
		console.log(user);
	});

	const [textInput, setTextInput] = useState([{name: '', surname: '', username: '' }]);

	const handleFormChange = (index, event) => {
		let data = [...textInput];
		data[index][event.target.name] = event.target.value;
		setTextInput(data);
	};

	const deleteUser = (index) => {
		let data = [...textInput];
		data.splice(index, 1);
		setTextInput(data);
	};

	return (
		<Box p={50} ml={180} mt={20}>
			<Flex ml={280}>
				<Box mr={280}>
					First Name
				</Box>
				<Box mr={210}>
					Last Name
				</Box>
				<Box mr={83}>
					Username
				</Box>
			</Flex>
			{textInput.map((attr, index) => {return (
				<HStack spacing={6} key={index}>
					<FormControl isRequired>
						<Box color ='black'>
							<Input  bg = 'white' placeholder='Name' left={215} width={200} type='text' defaultValue={attr.name} onChange={event => handleFormChange(index, event)} name="name"/>
							<FormLabel color = 'white' ml={280}> required </FormLabel>
						</Box>
					</FormControl>
					<FormControl isRequired>
						<Box color ='black'>
							<Input  bg = 'white' placeholder='Surname' left={25} width={200} type='text' defaultValue={attr.surname} onChange={event => handleFormChange(index, event)} name="surname"/>
							<FormLabel color = 'white' ml={100}> required </FormLabel>
						</Box>
					</FormControl>
					<FormControl isRequired>
						<Box color ='black'>
							<InputGroup right={180} width={200} type='text' >
								<InputLeftAddon children='#' />
								<Input bg='white' placeholder='Username' defaultValue={attr.username} onChange={event => handleFormChange(index, event)} name="username"/>
							</InputGroup>
							<FormLabel color = 'white'> required </FormLabel>
						</Box>
					</FormControl>
				</HStack>
			);})}
			<Flex mt={8} ml={280}>
				<Box mr={280}>
					Access Level
				</Box>
				<Box mr={210}>
					Role
				</Box>
			</Flex>
			<HStack ml={280}>
				<Box>
					<Select placeholder='Select Access Level' color='black' bg='white' right={61} width={200}>
						<option value='option1'>Option 1</option>
						<option value='option2'>Option 2</option>
						<option value='option3'>Option 3</option>
					</Select>
				</Box>
				<Box>
					<Select placeholder='Select Role' color='black' bg='white' left={79} width={200}>
						<option value='option1'>Option 1</option>
						<option value='option2'>Option 2</option>
						<option value='option3'>Option 3</option>
					</Select>
				</Box>
			</HStack>
			<Stack direction='row' spacing={4} align='center' mt={14} ml={280}>
				<Button colorScheme='blue' variant='solid' size='lg'>
					Save
				</Button>
				<Button colorScheme='red' variant='solid' size='lg' left={70}>
					Delete
				</Button>
			</Stack>
		</Box>
	);
};

export default User;
