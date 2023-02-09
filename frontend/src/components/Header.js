import { Box, Button, HStack, Link } from '@chakra-ui/react';
import { NavLink } from 'react-router-dom';
import CustomNavLink from './CustomNavLink';
import UserMenuButton from './UserMenuButton';

const Header = () => {
	return ( 
		<Box>
			<HStack>
				<CustomNavLink to="filter">
				filter
				</CustomNavLink>
				<CustomNavLink to="assets">
				assets
				</CustomNavLink>
				<Link>Hello</Link>
				<UserMenuButton />
			</HStack>
			
		</Box> );
};
 
export default Header;