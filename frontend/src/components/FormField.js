import {
	FormControl,
	FormLabel,
	Editable,
	EditablePreview,
	EditableInput,
	Input,
	Checkbox,
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
		<FormControl >
			<FormLabel textTransform='capitalize'>{fieldName}</FormLabel>
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
					<Input type={fieldType} as={EditableInput} />
					<EditableControls />
				</Editable>
			)}
		</FormControl>
	);
};

export default FormField;
