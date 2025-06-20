import {
	FormControl,
	FormLabel,
	Editable,
	EditablePreview,
	EditableInput,
	Input,
	Checkbox,
	Alert,
	AlertDescription,
	AlertIcon,
	AlertTitle,
	Box,
	EditableTextarea
} from '@chakra-ui/react';
import { useEffect, useState } from 'react';
import EditableControls from './EditableControls';
const FormField = ({
	children,
	fieldName,
	fieldType,
	fieldDefaultValue,
	isDisabled,
	onSubmitHandler,
	clearOnSumbit,
	trigger,
	validation,
	setErrorCount,
	isTextarea
}) => {
	const [error, setError] = useState('');
	const [value,setValue]=useState('');
	const validate=(e)=>{
		let err=e.target.validationMessage;
		setValue(e.target.value);
		if(err.length===0 && error.length>0){
			setErrorCount((prev)=>prev-1);
		}
		if(err.length>0 && error.length===0){
			setErrorCount((prev)=>prev+1);
		}
		setError(err);
	};

	const handleSumbit=(e)=>{
		if (error===''){
			onSubmitHandler(fieldName, e);
			if(clearOnSumbit){
				setValue('');
			}
		}
	};
	useEffect(() => {
		if(!clearOnSumbit){
			setValue(fieldDefaultValue);
		}
	}, [trigger,clearOnSumbit]);
	



	return (
		<FormControl isRequired={!(validation && validation.isOptional)}>
			<FormLabel>{fieldName}</FormLabel>
			{children}
			{fieldType === 'checkbox' ? (
				<Checkbox
					isDisabled={isDisabled}
					defaultChecked={fieldDefaultValue}
					onChange={(e) => {
						onSubmitHandler(fieldName, e.target.checked);
					}}
				/>
			) : (
				<Editable
					textAlign="center"
					defaultValue={fieldDefaultValue}
					isDisabled={isDisabled}	
					submitOnBlur={true}
					alignItems='left' 
					alignContent='left'
					paddingBottom={1}
					paddingRight={5}
					// border={'1px solid'}
					onSubmit={(e) => {
						handleSumbit(e);
					}}
					value={value}
				>
		
					<EditablePreview background={value.length?'blue.100':undefined} px={2} minW={'100%'} alignItems='left'
						alignContent='left' textAlign='left' />
				
					{isTextarea ? <EditableTextarea  onChange={e=>{setValue(e.target.value);}} textAlign='left' />:<Input type={fieldType} as={EditableInput} onChange={e=>{validate(e);}}  textAlign='left' />}
			
					<EditableControls error={error}/>
	
					
	
					
		
				</Editable>
			)}
			{error!=='' && (<Alert status='warning'>
  							<AlertIcon />
				<AlertTitle>Validation Error</AlertTitle>
				<AlertDescription>{error}</AlertDescription>
			</Alert>)}
		</FormControl>
	);
};

export default FormField;
