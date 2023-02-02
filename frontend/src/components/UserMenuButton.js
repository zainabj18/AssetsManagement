import { Menu,MenuButton,MenuList,Button,MenuItem} from '@chakra-ui/react';
import { FaUserCircle } from 'react-icons/fa';
import useAuth from '../hooks/useAuth';
const UserMenuButton = () => {
	const {user} = useAuth();
	return ( <Menu>
		<MenuButton as={Button} colorScheme='pink' leftIcon={<FaUserCircle size={18} />}>
			{user.username}
		</MenuButton>

		<MenuList>
			<MenuItem>Logout</MenuItem>
		</MenuList>
	</Menu>);
};
 
export default UserMenuButton;