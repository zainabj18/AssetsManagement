import {
	Button, Tag, TagLabel, Wrap, TagCloseButton, Input, FormControl, FormLabel, FormErrorMessage
} from '@chakra-ui/react';
import { useState } from 'react';

const List = ({ insertInto_new_attribute_data, attribute, attributeIndex, isInvalid, errorMessage }) => {
	const [inputField, set_inputField] = useState('');
	const [data, set_data] = useState([]);
	return (
		<FormControl isInvalid={isInvalid}>
			<FormLabel>{attribute.attributeName}</FormLabel>
			<FormErrorMessage>{errorMessage}</FormErrorMessage>
			<Wrap spacing={4}>
				{data.map((entry, index) => {
					return (
						<Tag key={index}>
							<TagLabel>{entry}</TagLabel>
							<TagCloseButton onClick={() => {
								let newData = data;
								newData.splice(index, 1);
								insertInto_new_attribute_data(newData, attributeIndex);
								set_data(newData);
							}} />
						</Tag>
					);
				})}
			</Wrap>
			<Input
				type={attribute.validation.type}
				placeholder='New Entry'
				onChange={(e) => set_inputField(e.target.value)}
			/>
			<Button onClick={() => {
				let newData = data;
				newData.push(inputField);
				insertInto_new_attribute_data(newData, attributeIndex);
				set_data(newData);
			}}>Add</Button>
		</FormControl>
	);
};

export default List;