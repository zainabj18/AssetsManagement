import {
	FormControl,
	FormLabel,
	NumberInput,
	NumberInputField,
	NumberInputStepper,
	NumberIncrementStepper,
	NumberDecrementStepper,
	FormHelperText
} from '@chakra-ui/react';

const NumFormField = ({fieldName,fieldDefaultValue,validation,onChangeHandler,isDisabled}) => {
	return (
		<FormControl >
			<FormLabel>{fieldName}</FormLabel>
			<NumberInput 
				defaultValue={fieldDefaultValue} 
				min={validation.min} 
				max={validation.max} 
				onChange={(val) => onChangeHandler(fieldName,val)}
				isDisabled={isDisabled}
			>
				<NumberInputField />
				<NumberInputStepper >
					<NumberIncrementStepper color={'blue.100'}/>
					<NumberDecrementStepper color={'blue.100'}/>
				</NumberInputStepper>
				<FormHelperText color={'white'}>Please enter a number between {validation.min} to {validation.max}.</FormHelperText>
			</NumberInput>
		</FormControl>
	);
};

export default NumFormField;
