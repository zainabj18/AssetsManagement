import { Outlet,redirect} from 'react-router-dom';
import { Container, Heading, VStack,Text ,Box} from '@chakra-ui/react';
import useAuth from '../hooks/useAuth';
import UserMenuButton from '../components/UserMenuButton';
import { useEffect } from 'react';
import Header from '../components/Header';

const styles={
	background:'white',
	 borderRadius:"0 0 12px 12px",
	boxShadow:"0 3px 6px #00000029" ,
	borderTopRadius:"0",
  borderRightRadius:"0",
  borderLeftRadius:"0",
  borderBottomRadius:"12px",
  boxShadow:"0 3px 6px #00000029",
  display:"flex",
  alignItem:"center",
  justifyContent: "space-between",
  paddingY:2
  
}
const Layout = () => {
	const {loggedIn,user} = useAuth();
	useEffect(() => {
		if (!loggedIn ||!user){
			redirect('/login');
		}
	},[loggedIn,user]);

	return (
		<VStack minW="100vw" minH={'100vh'} p={1} m={1}>
			<Heading marginY={2} textAlign="center">Code Groover Assets Metadata Repository</Heading>

			<Box sx={styles} width="90vw" >
			<Header />
			<Box display={'flex'} flexDirection="row" justifyContent={"center"} marginX={2} >
			<Text marginX={4} >Hello</Text>
				<UserMenuButton />
				</Box>
			</Box>

			
			<Container maxW={'full'} alignContent="center" display={'flex'} justifyContent="center" flexDirection={'column'} width={"60vw"}  >
				<Outlet />
			</Container>
		</VStack>
	);
};

export default Layout;
