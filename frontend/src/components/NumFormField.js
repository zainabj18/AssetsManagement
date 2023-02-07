import {
	FormControl,
	FormLabel,
	NumberInput,
	NumberInputField,
	NumberInputStepper,
	NumberIncrementStepper,
	NumberDecrementStepper
} from '@chakra-ui/react';

const NumFormField = ({fieldName,fieldDefaultValue,validation}) => {
	return (
		<FormControl bg="white" color="black" borderRadius="5" border="3" borderColor='gray.200' padding={6}>
			<FormLabel textTransform='capitalize'>{fieldName}</FormLabel>
			<NumberInput defaultValue={fieldDefaultValue} min={1} max={validation.max}>
				<NumberInputField />
				<NumberInputStepper >
					<NumberIncrementStepper color={'blue.100'}/>
					<NumberDecrementStepper color={'blue.100'}/>
				</NumberInputStepper>
			</NumberInput>
		</FormControl>
	);
};

export default NumFormField;
