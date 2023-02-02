import { Box, Button, Link } from '@chakra-ui/react';
import { NavLink } from 'react-router-dom';

const Header = ({logout}) => {

	return ( 
		<Box>
			<Link as={NavLink} to="assets">Assets</Link>
			<Button onClick={logout}>Logout</Button>
		</Box> );
};
 
export default Header;