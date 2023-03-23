import { Menu,MenuButton,MenuList,Button,MenuItem,MenuGroup,MenuDivider, Badge, HStack} from '@chakra-ui/react';
import { useEffect } from 'react';
import { FaUserCircle } from 'react-icons/fa';
import { MdLogout } from 'react-icons/md';
import { NavLink, useNavigate } from 'react-router-dom';
import useAuth from '../../hooks/useAuth';
import CustomNavLink from '../CustomNavLink';
const UserMenuButton = () => {
	const {user,logout} = useAuth();
	let naviagte=useNavigate();
	useEffect(() => {
	  if(!user){
			naviagte('/login');
	  }

	}, [user]);
	
	return (user &&( <Menu bg="white">
		<MenuButton as={Button} colorScheme='pink' leftIcon={<FaUserCircle size={18} />}>
			{user.username}
		</MenuButton>

		<MenuList color='white' >
			<MenuGroup title='Profile'>
				<HStack p={1}>
					<Badge bg={user.userRole} color="white">{user.userRole}</Badge>
					<Badge bg={user.userPrivileges} color="white">{user.userPrivileges}</Badge>
				</HStack>
			
				<MenuItem as={NavLink} to="/assets/my">My assets</MenuItem>
	
				
			</MenuGroup>
			<MenuDivider />
			<MenuItem onClick={logout} icon={<MdLogout />}>Logout</MenuItem>
		</MenuList>

	</Menu>));
};
 
export default UserMenuButton;