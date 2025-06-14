import {
	FormControl,
	FormLabel,
	Wrap,
	WrapItem,
	Tag,
	TagLabel,
	TagCloseButton,
	Button,
	Input,
	useBoolean
} from '@chakra-ui/react';
import { useState,useEffect} from 'react';
import FormField from './FormField';
const ListFormField = ({fieldName,fieldDefaultValue,validation,onChangeHandler,setErrorCount,isDisabled}) => {
	const [values, setValues] = useState([]);

	const addHandler=(newVal)=>{
		console.log('I am adding new value');
		if (values && !values.some(val => val===newVal)){
			let newValues = [...values, newVal];
			onChangeHandler(fieldName,newValues);
			setValues(newValues);
		}
	};

	const deleteHandler=(e,value)=>{
		let newValues = values.filter((val) => val !== value);
		onChangeHandler(fieldName,newValues);
		setValues(newValues);
	};

	useEffect(() => {
		setValues(fieldDefaultValue);
	}, []);
	

	return (
		<>
			<FormField
				fieldName={fieldName}
				fieldType={validation.type}
				fieldDefaultValue={''}
				isDisabled={isDisabled}
				onSubmitHandler={(_,val)=>{addHandler(val);}}
				clearOnSumbit={true}
				setErrorCount={setErrorCount}
			>
				<Wrap spacing={4}>
					{values&&values.map((value, key) => (
						<WrapItem key={key}>
							<Tag key={key}>
								<TagLabel>{value}</TagLabel>
								{!isDisabled && <TagCloseButton onClick={(e) => deleteHandler(e,value)} />}	
							</Tag>
						</WrapItem>
					))}
				</Wrap>
			</FormField>
			
		</>
	);
};

export default ListFormField;
