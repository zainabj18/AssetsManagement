import { Link } from '@chakra-ui/react';
import { NavLink } from 'react-router-dom';
const CustomNavLink = ({ children, to, ...props }) => {
	const activeStyle={
		textDecoration: 'underline',
	};
	return (
		<Link as={NavLink} variant='nav' style={({ isActive }) => isActive ? activeStyle : undefined} to={to} {...props}>
			{children}
		</Link>
	);
};

export default CustomNavLink;
