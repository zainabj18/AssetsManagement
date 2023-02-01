import { Outlet,useNavigate} from 'react-router-dom';
import { Container, Heading, VStack } from '@chakra-ui/react';
import useAuth from '../hooks/useAuth';
import { useEffect } from 'react';
const Layout = () => {
	const {loggedIn} = useAuth();
	let navigate = useNavigate();
	useEffect(() => {
		console.log(loggedIn);
		if (!loggedIn){
			navigate('/login');
		}
	},[loggedIn]);
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
