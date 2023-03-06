import { VStack, Checkbox, Text, FormControl, FormLabel, FormErrorMessage } from '@chakra-ui/react';

const Options = ({ new_attribute_data, insertInto_new_attribute_data, attribute, attributeIndex, isInvalid, errorMessage }) => {
	const ajustChecked = (checked, value) => {
		let list;
		if (!attribute.validation.isMulti) {
			list = [value];
		}
		else {
			list = new_attribute_data[attributeIndex];
			if (checked) {
				list.push(value);
			}
			else {
				let index = list.indexOf(value);
				list.splice(index, 1);
			}
		}
		insertInto_new_attribute_data(list, attributeIndex);
	};

	const checkChecked = (value) => {
		return new_attribute_data[attributeIndex].includes(value);

	};

	return (
		<FormControl isInvalid={isInvalid}>
			<FormLabel>{attribute.attributeName}</FormLabel>
			<FormErrorMessage>{errorMessage}</FormErrorMessage>
			{attribute.validation.values.map((value, index) => {
				return (
					<Checkbox
						key={index}
						isChecked={checkChecked(value)}
						onChange={(e) => ajustChecked(e.target.checked, value)}
					>{value}</Checkbox>
				);
			})}
		</FormControl>
	);
};

export default Options;