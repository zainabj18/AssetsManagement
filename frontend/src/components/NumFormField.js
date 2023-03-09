import {
	FormControl,
	FormLabel,
	NumberInput,
	NumberInputField,
	NumberInputStepper,
	NumberIncrementStepper,
	NumberDecrementStepper
} from '@chakra-ui/react';

const NumFormField = ({fieldName,fieldDefaultValue,validation,onChangeHandler,isDisabled}) => {
	return (
		<FormControl >
			<FormLabel>{fieldName}</FormLabel>
			<NumberInput 
				defaultValue={fieldDefaultValue} 
				min={1} 
				max={validation.max} 
				onChange={(val) => onChangeHandler(fieldName,val)}
				isDisabled={isDisabled}
			>
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
