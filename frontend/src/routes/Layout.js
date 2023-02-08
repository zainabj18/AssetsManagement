import { Outlet,useNavigate} from 'react-router-dom';
import { Container, Heading, VStack,Spinner } from '@chakra-ui/react';
import { useEffect } from 'react';
import Header from '../components/Header';

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
