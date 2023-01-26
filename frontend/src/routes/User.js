import { Input, VStack } from '@chakra-ui/react';
import { Box } from '@chakra-ui/react';
import { Text } from '@chakra-ui/react';
import { React } from 'react';

const User = () => {
	return (
		<VStack>
			<Box mb={6} mr={900}>
				First Name
			</Box>
			<Box mt={5} mr={900}>
				Last Name
			</Box>
			<Box color ='black'>
				<Input  bg = 'white' placeholder='Name' top={3} right={450}/>
			</Box>
			<Box color ='black'>
				<Input  bg = 'white' bottom={9} placeholder='Surname'/>
			</Box>
		</VStack>
	);
};

export default User;
