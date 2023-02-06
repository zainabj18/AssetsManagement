import {
	FormControl,
	FormLabel,
	Wrap,
	WrapItem,
	Tag,
	TagLabel,
	Button,
	Select,
	Menu,
	MenuButton,
	MenuList,
	MenuOptionGroup,
	MenuItemOption
} from '@chakra-ui/react';
import { useState } from 'react';
const SelectFormField = ({}) => {

	const [values, setValues] = useState([]);

	return (
		<FormControl bg="white" color="black" borderRadius="5" border="3" borderColor='gray.200' padding={6}>
			<FormLabel>Project</FormLabel>
			<Select placeholder='Select option' />
			<Wrap spacing={4}>
				{values.map((value, key) => (
					<WrapItem key={key}>
						<Tag size={'md'} key={key}>
							<TagLabel>{value.name}</TagLabel>
						</Tag>
					</WrapItem>
				))}
			</Wrap>
			<Menu closeOnSelect={false}>
				<MenuButton as={Button} colorScheme='blue'>
					MenuItem
				</MenuButton>
				<MenuList>
					<MenuOptionGroup type='checkbox' onChange={(e)=>{console.log(e);}}>
						<MenuItemOption value='1'>1</MenuItemOption>
						<MenuItemOption value='2'>2</MenuItemOption>
					</MenuOptionGroup>
				</MenuList>
			</Menu>
		</FormControl>
	);
};

export default SelectFormField;
