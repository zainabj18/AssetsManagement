import {
	NumberInput, NumberInputField, NumberInputStepper, NumberIncrementStepper, NumberDecrementStepper, FormControl, FormLabel, FormErrorMessage
} from '@chakra-ui/react';

const Num_Lmt = ({ new_attribute_data, insertInto_new_attribute_data, attribute, attributeIndex, isInvalid, errorMessage }) => {
	return (
		<FormControl isInvalid={isInvalid}>
			<FormLabel>{attribute.attributeName}</FormLabel>
			<FormErrorMessage>{errorMessage}</FormErrorMessage>
			<NumberInput
				min={attribute.validation.min}
				max={attribute.validation.max}
				value={new_attribute_data[attributeIndex]}
				onChange={(valueString) => insertInto_new_attribute_data(
					valueString, attributeIndex
				)}
			>
				<NumberInputField />
				<NumberInputStepper>
					<NumberIncrementStepper />
					<NumberDecrementStepper />
				</NumberInputStepper>
			</NumberInput>
		</FormControl>
	);
};

export default Num_Lmt;