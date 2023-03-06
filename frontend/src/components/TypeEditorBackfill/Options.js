import { VStack, Checkbox, Text } from '@chakra-ui/react';

const Options = ({ new_attribute_data, insertInto_new_attribute_data, attribute, attributeIndex }) => {
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
		<VStack align='left'>
			<Text>{attribute.attributeName}</Text>
			{attribute.validation.values.map((value, index) => {
				return (
					<Checkbox
						key={index}
						isChecked={checkChecked(value)}
						onChange={(e) => ajustChecked(e.target.checked, value)}
					>{value}</Checkbox>
				);
			})}
		</VStack>
	);
};

export default Options;