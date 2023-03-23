import { Link } from '@chakra-ui/react';
import { NavLink } from 'react-router-dom';

const CustomNavLink = ({ children, to, ...props }) => {

	const activeStyle={
		textDecoration: 'none',
		background:'#0a2861',
		color:'#fff',
		paddingY:0,
		marginY:0
		
	};
	

	return (
		<Link as={NavLink} variant='nav' style={({ isActive }) => isActive ? activeStyle :undefined } padding={3} marginX={2} to={to} {...props}>
			{children}
		</Link>
	);
};

export default CustomNavLink;
// 4a4a4a