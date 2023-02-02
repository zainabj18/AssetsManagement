import { Menu,MenuButton,MenuList,Button,MenuItem} from '@chakra-ui/react';
import { FaUserCircle } from 'react-icons/fa';
const UserMenuButton = () => {
	return ( <Menu>
		<MenuButton as={Button} colorScheme='pink' leftIcon={<FaUserCircle size={18} />}>
            Profile
		</MenuButton>

		<MenuList>
			<MenuItem>Logout</MenuItem>
		</MenuList>
	</Menu>);
};
 
export default UserMenuButton;