import {
	Checkbox,
	FormControl, FormLabel, FormErrorMessage,
	VStack,
} from '@chakra-ui/react';
import React, { useEffect, useState } from 'react';
import TypeAdderManager from '../components/TypeAdderManager';
import { fetchAllAttributes } from '../api';

const AttributeSelection = ({ selectedAttributes_state, set_selectedAttributes_state, load_attribute_trigger, isInvalid, isRequired, width }) => {

	useEffect(() => {
		async function load_allAttributes() {
			let data = await fetchAllAttributes(res => res.data);
			set_allAttributes(data);
		}
		load_allAttributes();
	}, [load_attribute_trigger]);

	const [allAttributes, set_allAttributes] = useState([]);

	const [selectedAttributes, set_selectedAttributes] = useState([]);

	useEffect(() => {
		set_selectedAttributes(selectedAttributes_state);
	}, [selectedAttributes_state]);

	const selectAttribute = (attribute) => {
		let list = [...selectedAttributes];
		list.push(attribute);
		set_selectedAttributes_state(TypeAdderManager.sortAttributes(list));
	};

	const deselectAttribute = (attribute) => {
		let selectedData = [...selectedAttributes];
		let index = selectedData.indexOf(attribute);
		selectedData.splice(index, 1);
		set_selectedAttributes_state(selectedData);
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
		console.log(selectedAttributes);
		if (typeof selectedAttributes !== 'undefined') {
			return TypeAdderManager.isAttributeNameIn(name, [...selectedAttributes]);
		}
		else {
			return false;
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