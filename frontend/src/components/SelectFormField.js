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
const SelectFormField = ({fieldName,fieldDefaultValue,validation,onChangeHandler,isDisabled}) => {

	const [values, setValues] = useState([]);
	const [options, setOptions] = useState([]);
	const [type, setType] = useState(null);

	const handleChange=(newValues)=>{
		console.log('hello');
		// if (type==='radio'){
		// 	console.log('hello');
		// 	newValues=newValues;	
		// }
		setValues(newValues);
		console.log('I am changing');
		onChangeHandler(fieldName,newValues);
	};

	useEffect(() => {
	  if (!validation.isMulti){
			setType('radio');
			console.log('I am raio');
			if (fieldDefaultValue){
				setValues([fieldDefaultValue]);
			}
	  }else{
			setType('checkbox');
			if (fieldDefaultValue){
				setValues([fieldDefaultValue]);
			}	
	  }
	  setOptions(validation.values);
	}, []);
	

	return (
		<FormControl >
			<FormLabel >{fieldName}</FormLabel>
			<Wrap spacing={4}>
				{values && values.map((value, key) => (
					<WrapItem key={key}>
						<Tag  key={key}>
							<TagLabel>{value}</TagLabel>
						</Tag>
					</WrapItem>
				))}
			</Wrap>
			{!isDisabled && <Menu closeOnSelect={false} >
				<MenuButton as={Button} colorScheme='blue' color={'white'}>
					Select {fieldName}
				</MenuButton>
				{type && <MenuList color={'white'}>	
					<MenuOptionGroup type={type} onChange={handleChange} defaultValue={fieldDefaultValue} >
						{options.map((value, key) => (
							<MenuItemOption key={key} value={value} color={'white'}>{value}</MenuItemOption>
						))}
					</MenuOptionGroup>
				</MenuList>}
			</Menu>}
			
		</FormControl>
	);
};

export default SelectFormField;
