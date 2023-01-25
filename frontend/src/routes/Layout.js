import { Outlet } from 'react-router-dom';
import { Heading, VStack, Container } from '@chakra-ui/react';

const Layout = () => {
	return (
		<VStack minW="100vw">
			<Heading>Code Groover Assets Metadata Repository</Heading>
			<Container minW={'100%'}>
				<Outlet />
			</Container>
		</VStack>
	);
};

export default Layout;
