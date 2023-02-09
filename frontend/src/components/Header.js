import { Box, HStack,Text } from '@chakra-ui/react';
import useAuth from '../hooks/useAuth';
import CustomNavLink from './CustomNavLink';
import UserMenuButton from './UserMenuButton';

const Header = () => {
	const {user} = useAuth();
	return ( 
		<Box>
			<HStack>
				<CustomNavLink to="assets/">
				Assets
				</CustomNavLink>
				<CustomNavLink to="type/">
				Types
				</CustomNavLink>
				<CustomNavLink to="projects/">
				Projects
				</CustomNavLink>
				{(user && user.userRole==='ADMIN') && <CustomNavLink to="accounts/">
				Accounts
				</CustomNavLink>}
				<Text>Hello</Text>
				<UserMenuButton />
			</HStack>
			
		</Box> );
};
 
export default Header;