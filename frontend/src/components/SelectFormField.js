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
import { useState,useEffect } from 'react';
const SelectFormField = ({fieldName,fieldDefaultValue,validation,onChangeHandler}) => {

	const [values, setValues] = useState([]);
	const [options, setOptions] = useState([]);
	const [type, setType] = useState(null);

	const handleChange=(newValues)=>{
		if (type==='radio'){
			newValues=[newValues];	
		}
		setValues(newValues);
		onChangeHandler(fieldDefaultValue,newValues);
	};

	useEffect(() => {
	  if (!validation.isMulti){
			setType('radio');
			console.log('I am multi');
			setValues([fieldDefaultValue]);
			
	  }else{
			setType('checkbox');
			setValues(fieldDefaultValue);
			
	  }
	  setOptions(validation.values);
	}, []);
	

	return (
		<FormControl >
			<FormLabel textTransform='capitalize'>{fieldName}</FormLabel>
			<Wrap spacing={4}>
				{values && values.map((value, key) => (
					<WrapItem key={key}>
						<Tag size={'md'} key={key}>
							<TagLabel>{value}</TagLabel>
						</Tag>
					</WrapItem>
				))}
			</Wrap>
			<Menu closeOnSelect={false}>
				<MenuButton as={Button} colorScheme='blue'>
					Select {fieldName}
				</MenuButton>
				{type && <MenuList>	
					<MenuOptionGroup type={type} onChange={handleChange} defaultValue={fieldDefaultValue}>
						{options.map((value, key) => (
							<MenuItemOption key={key} value={value}>{value}</MenuItemOption>
						))}
					</MenuOptionGroup>
				</MenuList>}
			</Menu>
		</FormControl>
	);
};

export default SelectFormField;
