
import {
	Button,
	Checkbox,
	FormControl, FormLabel,
	Input,
	HStack, VStack,
	Table, Thead, Tbody, Tr, Th, Td, TableContainer, TableCaption,
	Text
} from '@chakra-ui/react';
import React, { useState } from 'react';

const TypeAdder = () => {

	/** The selected attributes */
	const [selectedAttributes, setSelectedAttributes] = useState([
		{ priKey: '0', attrName: 'programming language', attrType: 'text' }
	]);

	/** All attributes */
	const [attributes, setAttributes] = useState([
		{ priKey: '0', attrName: 'programming language', attrType: 'text' },
		{ priKey: '1', attrName: 'country of origin', attrType: 'text' }
	]);

	/** Decides if the attribute needs to be added or removed from selected */
	const ajustSelectedAttributes = (checked, index) => {
		if (checked) {
			addAttribute(index);
		}
		if (!checked) {
			let attrData = [...attributes];
			removeAttr(attrData[index]);
		}
	};

	/** Adds an attribute to the selected attributes */
	const addAttribute = (attrindex) => {
		let data = [...attributes];
		setSelectedAttributes([...selectedAttributes, data[attrindex]]);
	};

	/** Removes an attribute from the selected attributes */
	const removeAttr = (attr) => {
		let selectedData = [...selectedAttributes];
		let index = selectedData.indexOf(attr);
		selectedData.splice(index, 1);
		setSelectedAttributes(selectedData);
	};

	/** Checks to see if the given priKey is also in the selected attributes
	 * and if so, checks the check box for it */
	function sameChecked(priKey) {
		let selectedData = [...selectedAttributes];
		let i;
		for (i = 0; i < selectedData.length; i++) {
			// eslint-disable-next-line
			if (priKey == selectedData[i].priKey) {
				return true;
			}
		}
		return false;
	};

	return (
		<VStack width="90vw">
			<Text>TypeAdder</Text>
			<FormControl isRequired>
				<FormLabel>Name</FormLabel>
				<Input type='text' placeholder='Name' />
			</FormControl>
			<HStack minW='80%'>
				{/** The list of all attributes */}
				<FormControl width='30%'>
					<FormLabel>Selet attributes</FormLabel>
					{attributes.map((attr, index) => {
						return (
							<VStack key={attr.priKey} align="left">
								<Checkbox
									isChecked={sameChecked(index)}
									value={attr.attrName}
									onChange={(e) => ajustSelectedAttributes(e.target.checked, index)}
								> {attr.attrName}
								</Checkbox>
							</VStack>
						);
					})}
				</FormControl>
				{/** The List of selected attributes */}
				<TableContainer width='70%'>
					<Table varient='simple'>
						<TableCaption placement='top'>Selected Attributes</TableCaption>
						<Thead>
							<Tr>
								<Th>Attribute Name</Th>
								<Th>Data Type</Th>
							</Tr>
						</Thead>
						<Tbody>
							{selectedAttributes.map((attr, index) => {
								return (
									<Tr key={attr.priKey}>
										<Td>{attr.attrName}</Td>
										<Td>{attr.attrType}</Td>
									</Tr>
								);
							})}
						</Tbody>
					</Table>
				</TableContainer>
			</HStack>
			<Button>Add</Button>
			<Button>Save</Button>
		</VStack>
	);
};

export default TypeAdder;
