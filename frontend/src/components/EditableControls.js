import { CheckIcon, CloseIcon, EditIcon } from '@chakra-ui/icons';
import {
	ButtonGroup,
	useEditableControls,
	useEditableState,
	IconButton,
} from '@chakra-ui/react';
import { useEffect } from 'react';
const EditableControls = (props) => {
	const {
		isEditing,
		getSubmitButtonProps,
		getCancelButtonProps,
		getEditButtonProps,
	} = useEditableControls();
	const { isDisabled } = useEditableState();
	useEffect(() => {
	}, [props.error]);
	
	return isDisabled ? null : isEditing ? (
		<ButtonGroup m={'2'} justifyContent="end" w="100%">
			{props.error==='' && <IconButton icon={<CheckIcon />} {...getSubmitButtonProps()} />}
			<IconButton icon={<CloseIcon />} {...getCancelButtonProps()} />
		</ButtonGroup>
	) : (
		<ButtonGroup m={'2'} justifyContent="end" w="100%">
			<IconButton icon={<EditIcon />} {...getEditButtonProps()} />
		</ButtonGroup>
	);
};

export default EditableControls;
