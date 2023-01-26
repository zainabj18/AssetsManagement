import { Outlet } from 'react-router-dom';
import { Container, Heading, VStack } from '@chakra-ui/react';

const Layout = () => {
	return (
		
		<VStack minW="100vw" bg="blue.600" minH={'100vh'}>
			<Heading>Code Groover Assets Metadata Repository</Heading>
			<Container maxW={'full'}>
				<Outlet />
			</Container>
		</VStack>
	);
};

export default Layout;
