import { Box, HStack,Text } from '@chakra-ui/react';
import CustomNavLink from './CustomNavLink';
import UserMenuButton from './UserMenuButton';

const Header = () => {
	return ( 
		<Box>
			<HStack>
				<CustomNavLink to="type/">
				Types
				</CustomNavLink>
				<CustomNavLink to="assets/">
				Assets
				</CustomNavLink>
				<CustomNavLink to="projects/">
				Projects
				</CustomNavLink>
				<Text>Hello</Text>
				<UserMenuButton />
			</HStack>
			
		</Box> );
};
 
export default Header;