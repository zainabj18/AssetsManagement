import { Input } from '@chakra-ui/react';
import { Box } from '@chakra-ui/react';
import { Text } from '@chakra-ui/react';
import { React } from 'react';

const User = () => {
	return (
		<div>
			<Text fontsize = '2x1'>First Name</Text>
			<Box color ='black'>
				<Input  bg = 'white' placeholder='Name' />
			</Box>
		</div>
	);
};

export default User;
