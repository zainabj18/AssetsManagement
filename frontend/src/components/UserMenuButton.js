import { Menu,MenuButton,MenuList,Button,MenuItem} from '@chakra-ui/react';

const UserMenuButton = () => {
	return ( <Menu>
		<MenuButton as={Button} colorScheme='pink'>
          Profile
		</MenuButton>
		<MenuList>
			<MenuItem>Logout</MenuItem>
		</MenuList>
	</Menu>);
};
 
export default UserMenuButton;