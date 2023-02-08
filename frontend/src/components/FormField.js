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
	AlertTitle
} from '@chakra-ui/react';
import { useEffect, useState } from 'react';
import EditableControls from './EditableControls';
const FormField = ({
	children,
	fieldName,
	fieldType,
	fieldDefaultValue,
	isDisabled,
	startWithEditView,
	onSubmitHandler,
	clearOnSumbit,
	trigger
}) => {
	const [error, setError] = useState('');
	const [value,setValue]=useState('');
	const validate=(e)=>{
		setValue(e.target.value);
		setError(e.target.validationMessage);
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
		<FormControl isRequired>
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
					startWithEditView={startWithEditView}
					isDisabled={isDisabled}	
					submitOnBlur={false}
					onSubmit={(e) => {
						handleSumbit(e);
					}}
					value={value}
				>
					<EditablePreview />
					<Input type={fieldType} as={EditableInput} onChange={e=>{validate(e);}} required />
					<EditableControls error={error}/>
				</Editable>
			)}
			{error!=='' && (<Alert status='error'>
  							<AlertIcon />
				<AlertTitle>Validation Error</AlertTitle>
				<AlertDescription>{error}</AlertDescription>
			</Alert>)}
		</FormControl>
	);
};

export default FormField;
