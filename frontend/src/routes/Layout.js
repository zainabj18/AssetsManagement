import { Outlet } from 'react-router-dom';
import { Heading, VStack } from '@chakra-ui/react';

const Layout = () => {
	return (
		<VStack minW="100vw">
			<Heading>Code Groover Assets Metadata Repository</Heading>
			<Outlet />
		</VStack>
	);
};

export default Layout;
