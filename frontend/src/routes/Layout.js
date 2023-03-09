import { Outlet,redirect} from 'react-router-dom';
import { Container, Heading, VStack,Spinner } from '@chakra-ui/react';
import useAuth from '../hooks/useAuth';
import { useEffect } from 'react';
import Header from '../components/Header';

const Layout = () => {
	const {loggedIn,user} = useAuth();
	useEffect(() => {
		if (!loggedIn ||!user){
			redirect('/login');
		}
	},[loggedIn,user]);
	return (
		<VStack minW="100vw" minH={'100vh'} p={2} m={4}>

			<Heading>Code Groover Assets Metadata Repository</Heading>
			<Header />

			<Container maxW={'full'}>
				<Outlet />
			</Container>
		</VStack>
	);
};

export default Layout;
