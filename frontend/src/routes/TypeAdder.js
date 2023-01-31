
import {
	Button,
	Checkbox,
	FormControl, FormLabel,
	IconButton,
	Input,
	HStack, VStack,
	Table, Thead, Tbody, Tr, Th, Td, TableContainer, TableCaption,
	Text
} from '@chakra-ui/react';
import React, { useState } from 'react';
import { DeleteIcon } from '@chakra-ui/icons';


const TypeAdder = () => {
	const [selectedAttributes, setSelectedAttributes] = useState([
	]);
	const [attributes, setAttributes] = useState([
		{ attrName: 'programming language', attrType: 'text' },
		{ attrName: 'country of origin', attrType: 'text' }
	]);
	const ajustSelectedAttributes = (checked, index) => {
		if (checked) {
			addAttribute(index);
		}
		if (!checked) {
			let attrData = [...attributes];
			removeAttrByEqualAttr(attrData[index]);
		}
	};
	const addAttribute = (attrindex) => {
		let data = [...attributes];
		setSelectedAttributes([...selectedAttributes, data[attrindex]]);
	};
	const removeAttrByEqualAttr = (attr) => {
		let selectedData = [...selectedAttributes];
		let index = selectedData.indexOf(attr);
		selectedData.splice(index, 1);
		setSelectedAttributes(selectedData);
	};
	const removeAttributeByIndex = (index) => {
		let data = [...selectedAttributes];
		data.splice(index, 1);
		setSelectedAttributes(data);
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
							<VStack key={index} align="left">
								<Checkbox
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
								<Th>Delete</Th>
							</Tr>
						</Thead>
						<Tbody>
							{selectedAttributes.map((attr, index) => {
								return (
									<Tr key={index}>
										<Td>{attr.attrName}</Td>
										<Td>{attr.attrType}</Td>
										<Td><IconButton
											icon={<DeleteIcon />}
											colorScheme='blue'
											onClick={event => removeAttributeByIndex(index)}
										/></Td>
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
