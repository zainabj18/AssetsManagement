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
import { useState } from 'react';
import EditableControls from './EditableControls';
const FormField = ({
	fieldName,
	fieldType,
	fieldDefaultValue,
	isDisabled,
	startWithEditView,
	onSubmitHandler,
}) => {
	const [error, setError] = useState('');
	const validate=(e)=>{

		setError(e.target.validationMessage);
	};

	return (
		<FormControl isRequired>
			<FormLabel>{fieldName}</FormLabel>
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
					onSubmit={(e) => {
						onSubmitHandler(fieldName, e);
					}}
				>
					<EditablePreview />
					<Input type={fieldType} as={EditableInput} onChange={e=>{validate(e);}} required/>
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
