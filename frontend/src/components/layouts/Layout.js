import { Heading, VStack, Text, Box } from '@chakra-ui/react';
import useAuth from '../../hooks/useAuth';
import UserMenuButton from '../navigation/UserMenuButton';
import { Navigate, Outlet, redirect } from 'react-router-dom';
import { useEffect } from 'react';
import Header from '../navigation/Header';

const styles = {
	background: 'white',
	borderRadius: '0 0 12px 12px',
	boxShadow: '0 3px 6px #00000029',
	borderTopRadius: '0',
	borderRightRadius: '0',
	borderLeftRadius: '0',
	borderBottomRadius: '12px',
	boxShadow: '0 3px 6px #00000029',
	display: 'flex',
	alignItem: 'center',
	justifyContent: 'space-between',
	paddingY: 2

};
const Layout = () => {
	const { loggedIn, user } = useAuth();
	useEffect(() => {
		if (!loggedIn || !user) {
			redirect('/login');
		}
	}, [loggedIn, user]);

	return (
		<VStack minW='100vw' height={'99vh'} p={1} m={1}>
			{!user &&
				<Navigate to='/login' replace={true} />
			}
			<Heading marginY={2} textAlign='center'>Code Groover Assets Metadata Repository</Heading>

			<Box sx={styles} width='90vw' >
				<Header />
				<Box display={'flex'} flexDirection='row' justifyContent={'center'} alignItems='center' marginX={2} >
					<Text marginRight={3} >Hello</Text>
					<UserMenuButton />
				</Box>
			</Box>

			<Box maxW={'full'} alignContent='center' display={'flex'} justifyContent='center' flexDirection={'column'} width={'60vw'}  >
				<Outlet />
			</Box>
		</VStack>
	);
};

export default Layout;
