import {
	FormControl,
	FormLabel,
	Wrap,
	WrapItem,
	Tag,
	TagLabel,
	TagCloseButton,
	Button,
	Input
} from '@chakra-ui/react';
import { useState,useEffect} from 'react';
const ListFormField = ({fieldName,fieldDefaultValue,validation}) => {
	const [value, setValue] = useState('');
	const [values, setValues] = useState([]);

	const addHandler=()=>{
		setValues([...values, value]);
		setValue(null);
	};

	const deleteHandler=(e,value)=>{
		let newValues = values.filter((val) => val !== value);
		setValues(newValues);
	};

	useEffect(() => {
		setValues(fieldDefaultValue);
	}, []);
	

	return (
		<FormControl  bg="white" color="black" borderRadius="5" border="3" borderColor='gray.200' padding={6} >
			<FormLabel>{fieldName}</FormLabel>
			<Wrap spacing={4}>
				{values.map((value, key) => (
					<WrapItem key={key}>
						<Tag size={'md'} key={key}>
							<TagLabel>{value}</TagLabel>
							<TagCloseButton onClick={(e) => deleteHandler(e,value)} />
						</Tag>
					</WrapItem>
				))}
			</Wrap>
			<Input type={validation.type} value={value} onChange={e=>{setValue(e.target.value);}}/>
			{value && <Button onClick={addHandler}>Add</Button>}
		</FormControl>
	);
};

export default ListFormField;
