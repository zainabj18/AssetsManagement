import {
	Checkbox,
	FormControl, FormLabel, FormErrorMessage,
	VStack,
} from '@chakra-ui/react';
import React, { useEffect, useState } from 'react';
import TypeAdderManager from '../components/TypeAdderManager';
import { fetchAllAttributes } from '../api';

const AttributeSelection = ({
	set_selectedAttributes_state,
	load_attribute_trigger,
	isInvalid,
	isRequired,
	width
}) => {

	const [allAttributes, set_allAttributes] = useState([]);
	const [selectedAttributes, set_selectedAttributes] = useState([]);

	useEffect(() => {
		set_selectedAttributes_state(selectedAttributes);
	}, [selectedAttributes]);

	useEffect(() => {
		async function load_allAttributes() {
			let data = await fetchAllAttributes(res => res.data);
			set_allAttributes(data);
		}
		load_allAttributes();
	}, [load_attribute_trigger]);

	const selectAttribute = (attribute) => {
		let list = [...selectedAttributes];
		list.push(attribute);
		set_selectedAttributes(TypeAdderManager.sortAttributes(list));
	};

	const deselectAttribute = (attribute) => {
		let selectedData = [...selectedAttributes];
		let index = selectedData.indexOf(attribute);
		selectedData.splice(index, 1);
		set_selectedAttributes(selectedData);
	};

	const ajustSelectedAttributes = (checked, index) => {
		if (checked) {
			selectAttribute([...allAttributes][index]);
		}
		if (!checked) {
			deselectAttribute([...allAttributes][index]);
		}
	};

	return (
		<FormControl isRequired={isRequired} isInvalid={isInvalid} width={width}>
			<FormLabel>Select Attributes</FormLabel>
			<FormErrorMessage>At least 1 attribute must be selected</FormErrorMessage>
			{allAttributes.map((attribute, index) => {
				return (
					<VStack key={attribute.attributeName} align="left">
						<Checkbox
							isChecked={TypeAdderManager.isAttributeNameIn(
								attribute.attributeName, [...selectedAttributes]
							)}
							value={attribute.attributeName}
							onChange={(e) => ajustSelectedAttributes(e.target.checked, index)}
						> {attribute.attributeName}
						</Checkbox>
					</VStack>
				);
			})}
		</FormControl>
	);
};

export default AttributeSelection;