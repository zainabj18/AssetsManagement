import { CheckIcon, CloseIcon, EditIcon } from '@chakra-ui/icons';
import {
	ButtonGroup,
	useEditableControls,
	useEditableState,
	IconButton,
} from '@chakra-ui/react';
const EditableControls = () => {
	const {
		isEditing,
		getSubmitButtonProps,
		getCancelButtonProps,
		getEditButtonProps,
	} = useEditableControls();
	const { isDisabled } = useEditableState();
	return isDisabled ? null : isEditing ? (
		<ButtonGroup>
			<IconButton icon={<CheckIcon />} {...getSubmitButtonProps()} />
			<IconButton icon={<CloseIcon />} {...getCancelButtonProps()} />
		</ButtonGroup>
	) : (
		<ButtonGroup>
			<IconButton icon={<EditIcon />} {...getEditButtonProps()} />
		</ButtonGroup>
	);
};

export default EditableControls;
