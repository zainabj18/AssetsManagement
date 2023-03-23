import {
	Checkbox,
	FormControl, FormLabel, FormErrorMessage,
	VStack,
} from '@chakra-ui/react';
import React, { useEffect, useState } from 'react';
import TypeMethodManager from '../components/TypeMethodManager';
import { fetchAllAttributes } from '../api';

const AttributeSelection = ({ selectedAttributes_state, set_selectedAttributes_state, load_attribute_trigger, isInvalid, isRequired, width }) => {

	useEffect(() => {
		async function load_allAttributes() {
			let data = await fetchAllAttributes(res => res.data);
			set_allAttributes(data.data);
		}
		load_allAttributes();
	}, [load_attribute_trigger]);

	const [allAttributes, set_allAttributes] = useState([]);

	const selectAttribute = (attribute) => {
		let list = [...selectedAttributes_state];
		list.push(attribute);
		set_selectedAttributes_state(TypeMethodManager.sortAttributes(list));
	};

	const deselectAttribute = (attribute) => {
		let selectedData = [...selectedAttributes_state];
		let index = TypeMethodManager.getAttributeIndex(selectedData, attribute);
		if (index >= 0) {
			selectedData.splice(index, 1);
			set_selectedAttributes_state(selectedData);
		}
		else {
			console.warn('Attribute not found when deselecting.');
		}
	};

	const ajustSelectedAttributes = (checked, index) => {
		if (checked) {
			selectAttribute([...allAttributes][index]);
		}
		if (!checked) {
			deselectAttribute([...allAttributes][index]);
		}
	};

	const checkChecked = (name) => {
		if (typeof selectedAttributes_state !== 'undefined') {
			return TypeMethodManager.isAttributeNameIn(name, [...selectedAttributes_state]);
		}
		else {
			return false;
		}
	};


	return (
		<FormControl isRequired={isRequired} isInvalid={isInvalid} width={width} bg='gray.300' paddingX={3}>
			<FormLabel>Select Attributes</FormLabel>
			<FormErrorMessage>At least 1 attribute must be selected</FormErrorMessage>
			{allAttributes.map((attribute, index) => {
				return (
					<VStack key={attribute.attributeName} align="left">
						<Checkbox
							marginY={2}
							isChecked={checkChecked(attribute.attributeName)}
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