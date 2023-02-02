import { Outlet,useNavigate} from 'react-router-dom';
import { Container, Heading, VStack,Spinner } from '@chakra-ui/react';
import useAuth from '../hooks/useAuth';
import { useEffect } from 'react';
import Header from '../components/Header';

const Layout = () => {
	const {loggedIn,logout} = useAuth();
	let navigate = useNavigate();
	useEffect(() => {
		if (!loggedIn){
			navigate('/login');
		}
	},[loggedIn]);
	return (
		<VStack minW="100vw" bg="blue.600" minH={'100vh'}>
			<Heading>Code Groover Assets Metadata Repository</Heading>
			<Header logout={logout}/>
			<Container maxW={'full'}>
				<Outlet />
			</Container>
		</VStack>
	);
};

export default Layout;
