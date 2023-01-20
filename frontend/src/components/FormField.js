import {
	FormControl,
	FormLabel,
	Editable,
	EditablePreview,
	EditableInput,
	Input,
} from '@chakra-ui/react';
import EditableControls from './EditableControls';
const FormField = ({
	fieldName,
	fieldType,
	fieldDefaultValue,
	isDisabled,
	startWithEditView,
	onSubmitHandler,
}) => {
	return (
		<FormControl bg="white" color="black">
			<FormLabel>{fieldName}</FormLabel>
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
				<Input type={fieldType} as={EditableInput} />
				<EditableControls />
			</Editable>
		</FormControl>
	);
};

export default FormField;
