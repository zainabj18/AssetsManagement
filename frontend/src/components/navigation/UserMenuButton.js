import { Menu,MenuButton,MenuList,Button,MenuItem,MenuGroup,MenuDivider, Badge, HStack} from '@chakra-ui/react';
import { useEffect } from 'react';
import { FaUserCircle } from 'react-icons/fa';
import { MdLogout } from 'react-icons/md';
import { useNavigate } from 'react-router-dom';
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
	
	return (user &&( <Menu>
		<MenuButton as={Button} colorScheme='pink' leftIcon={<FaUserCircle size={18} />}>
			{user.username}
		</MenuButton>

		<MenuList color='white'>
			<MenuGroup title='Profile'>
				<HStack>
					<Badge>{user.userRole}</Badge>
					<Badge>{user.userPrivileges}</Badge>
				</HStack>
			
				<MenuItem as={CustomNavLink} to="/assets/my">View related assets</MenuItem>
	
				
			</MenuGroup>
			<MenuDivider />
			<MenuItem onClick={logout} icon={<MdLogout />}>Logout</MenuItem>
		</MenuList>

	</Menu>));
};
 
export default UserMenuButton;