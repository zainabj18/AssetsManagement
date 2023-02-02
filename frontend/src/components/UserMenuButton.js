import { Menu,MenuButton,MenuList,Button,MenuItem,MenuGroup,MenuDivider, Badge, HStack} from '@chakra-ui/react';
import { FaUserCircle } from 'react-icons/fa';
import useAuth from '../hooks/useAuth';
const UserMenuButton = () => {
	const {user,logout} = useAuth();
	return ( <Menu>
		<MenuButton as={Button} colorScheme='pink' leftIcon={<FaUserCircle size={18} />}>
			{user.username}
		</MenuButton>

		<MenuList>
			<MenuGroup title='Profile'>
				<HStack>
					<Badge>{user.userRole}</Badge>
					<Badge>{user.userPrivileges}</Badge>
				</HStack>
				<MenuItem>View profile</MenuItem>
				<MenuItem>View related assets</MenuItem>
				<MenuItem>View related projects</MenuItem>
			</MenuGroup>
			<MenuDivider />
			<MenuItem onClick={logout}>Logout</MenuItem>
		</MenuList>

	</Menu>);
};
 
export default UserMenuButton;