import { Box, Button, HStack, Link } from '@chakra-ui/react';
import { NavLink } from 'react-router-dom';
import CustomNavLink from './CustomNavLink';

const Header = ({logout}) => {
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
				<Button onClick={logout}>Logout</Button>
			</HStack>
			
		</Box> );
};
 
export default Header;