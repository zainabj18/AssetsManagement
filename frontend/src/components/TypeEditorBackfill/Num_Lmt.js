import {
	NumberInput, NumberInputField, NumberInputStepper, NumberIncrementStepper, NumberDecrementStepper, Text
} from '@chakra-ui/react';

const Num_Lmt = ({ new_attribute_data, insertInto_new_attribute_data, attribute, attributeIndex }) => {
	return (
		<>
			<Text>{attribute.attributeName}</Text>
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
		</>
	);
};

export default Num_Lmt;