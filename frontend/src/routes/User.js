import { HStack, Input, VStack} from '@chakra-ui/react';
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
				<Box mr={105}>
					Username
				</Box>
			</Flex>
			<HStack>
				<Box color ='black'>
					<Input  bg = 'white' placeholder='Name' right={70}/>
				</Box>
				<Box color ='black'>
					<Input  bg = 'white' placeholder='Surname' left={71}/>
				</Box>
				<Box color ='black'>
					<InputGroup left={48}>
						<InputLeftAddon children='#' />
						<Input bg='white'/>
					</InputGroup>
				</Box>
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
					<Select placeholder='Select option' color='black' bg='white' right={7}>
						<option value='option1'>Option 1</option>
						<option value='option2'>Option 2</option>
						<option value='option3'>Option 3</option>
					</Select>
				</Box>
				<Box>
					<Select placeholder='Select option' color='black' bg='white' left={162}>
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
			</Stack>
		</Box>
	);
};

export default User;
