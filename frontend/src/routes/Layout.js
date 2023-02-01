import { Outlet,useNavigate} from 'react-router-dom';
import { Container, Heading, VStack } from '@chakra-ui/react';
import useAuth from '../hooks/useAuth';
import { useEffect } from 'react';
import Header from '../components/Header';

const Layout = () => {
	const {loaded,loggedIn} = useAuth();
	let navigate = useNavigate();
	useEffect(() => {
		console.log('layout mounted');
		console.log(loggedIn);
		if (loaded && !loggedIn){
			navigate('/login');
		}
	},[loggedIn]);
	return (
		<VStack minW="100vw" bg="blue.600" minH={'100vh'}>
			<Heading>Code Groover Assets Metadata Repository</Heading>
			<Header />
			<Container maxW={'full'}>
				<Outlet />
			</Container>
		</VStack>
	);
};

export default Layout;
