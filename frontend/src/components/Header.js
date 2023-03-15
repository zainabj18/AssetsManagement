import { Box, Flex, HStack,Spacer,Text } from '@chakra-ui/react';
import useAuth from '../hooks/useAuth';
import CustomNavLink from './CustomNavLink';
import UserMenuButton from './UserMenuButton';

const Header = () => {
	const {user} = useAuth();
	return ( 
		<Flex w={'70%'}>
			<HStack>
				<CustomNavLink to="assets/" >
				Assets
				</CustomNavLink>
				<CustomNavLink to="type/">
				Types
				</CustomNavLink>
				<CustomNavLink to="projects/">
				Projects
				</CustomNavLink>
				<CustomNavLink to="type/attributes/">
				Attributes
				</CustomNavLink>
				<CustomNavLink to="tags/">
				Tags
				</CustomNavLink>
				{(user && user.userRole==='ADMIN') && <CustomNavLink to="accounts/">
				Accounts
				</CustomNavLink>}
			</HStack>
			<Spacer />
			
		

			
		</Flex> );
};
 
export default Header;