import { FormControl, FormLabel, HStack, Input} from '@chakra-ui/react';
import { Box } from '@chakra-ui/react';
import { React } from 'react';
import { Flex, InputGroup, InputLeftAddon } from '@chakra-ui/react';
import { Select } from '@chakra-ui/react';
import { Stack, Button} from '@chakra-ui/react';

const User = () => {
	return (
		<Box p={50}>
			<Flex>
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
			<HStack spacing={5}>
				<FormControl isRequired>
					<Box color ='black'>
						<Input  bg = 'white' placeholder='Name' right={65} width={200} type='text'/>
						<FormLabel color = 'white'> required </FormLabel>
					</Box>
				</FormControl>
				<FormControl isRequired>
					<Box color ='black'>
						<Input  bg = 'white' placeholder='Surname' left={5} width={200} type='text'/>
						<FormLabel color = 'white'> required </FormLabel>
					</Box>
				</FormControl>
				<FormControl isRequired>
					<Box color ='black'>
						<InputGroup left={85} width={200 } type='text'>
							<InputLeftAddon children='#' />
							<Input bg='white'/>
						</InputGroup>
						<FormLabel color = 'white' right={50}> required </FormLabel>
					</Box>
				</FormControl>
			</HStack>
			<Flex mt={8}>
				<Box mr={280}>
					Access Level
				</Box>
				<Box mr={210}>
					Role
				</Box>
			</Flex>
			<HStack>
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
			<Stack direction='row' spacing={4} align='center' mt={14}>
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