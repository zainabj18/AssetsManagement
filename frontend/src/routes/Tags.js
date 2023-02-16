import { Box, Button, Flex, HStack, Input, } from '@chakra-ui/react';

const Tags = () => {
	return (<Flex w='100%' minH='80vh' alignItems={'stretch'} p={2} border>
		<HStack w='30%' minH='100%' bg='gray.300' p={4} color='black' align={'top'}>
			<Input type='text' placeholder='Search for tag ...'/>
			<Button>Create</Button>
		</HStack>
		<Box w='70%' minH='100%' bg='white' />
	</Flex>
	);
};
 
export default Tags;
