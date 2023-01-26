import { HStack, Input, VStack} from '@chakra-ui/react';
import { Box } from '@chakra-ui/react';
import { Text } from '@chakra-ui/react';
import { React } from 'react';
import { Flex, InputGroup, InputLeftAddon } from '@chakra-ui/react';

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
		</Box>
	);
};

export default User;
