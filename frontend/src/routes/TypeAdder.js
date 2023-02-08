
import {
	Button,
	Checkbox,
	FormControl, FormLabel, FormErrorMessage,
	Input,
	HStack, VStack,
	Modal, ModalOverlay, ModalContent, ModalHeader, ModalCloseButton, ModalBody, ModalFooter,
	Select,
	Table, Thead, Tbody, Tr, Th, Td, TableContainer, TableCaption,
	Text,
	useDisclosure
} from '@chakra-ui/react';
import React, { useEffect, useState } from 'react';
import AttributeMaker from '../components/AttributeMaker';
import AttributeManager from '../components/AttributeManager';

import { fetchAllAttributes } from '../api';

const TypeAdder = () => {

	useEffect(() => {
		async function load_allAssets() {
			let data = await fetchAllAttributes(res => res.data);
			set_allAttributes(data);
		}
		load_allAssets();
	}, []);

	const {
		isOpen: isOpen_attributeCreator,
		onOpen: onOpen_attributeCreator,
		onClose: onClose_attributeCreator
	} = useDisclosure();

	const [types] = useState([
		'text', 'number', 'checkbox', 'datetime-local', 'num_lmt', 'options', 'list'
	]);

	const [selectedAttributes, set_selectedAttributes] = useState([
		/** Dummy Data */
		{
			attributeName: 'public',
			attributeType: 'checkbox',
		},
		{
			attributeName: 'license',
			attributeType: 'options',
			validation: {
				values: ['MIT', 'GNU'],
				isMulti: true
			}
		},
		{
			attributeName: 'programming Language(s)',
			attributeType: 'text',
		}
		/** End of Dummy Data */
	]);
	const [allAttributes, set_allAttributes] = useState(
		[]
	);
	const [creationData, set_creationData] = useState(new AttributeMaker());
	const [new_attribute_errorMessage, set_new_attribute_errorMessage] = useState(AttributeMaker.get_message_noError());
	const [display_num_lmt, set_display_num_lmt] = useState(false);

	const selectAttribute = (attribute) => {
		let list = [...selectedAttributes];
		list.push(attribute);
		set_selectedAttributes(AttributeManager.sortAttributes(list));
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

	const updateSelectedTypes = (data = creationData) => {
		set_display_num_lmt(data.type === 'num_lmt');
	};

	const open_AttributeCreator = () => {
		let new_data = new AttributeMaker();
		new_data.type = types[0];
		updateSelectedTypes(new_data);
		set_new_attribute_errorMessage(AttributeMaker.get_message_noError());
		set_creationData(new_data);
		onOpen_attributeCreator();
	};

	const tryCreate_attribute = () => {
		let errorMessage = creationData.checkForErrors([...allAttributes]);
		set_new_attribute_errorMessage(errorMessage);
		if (JSON.stringify(errorMessage) === JSON.stringify(AttributeMaker.get_message_noError())) {
			let new_attribute = creationData.formAttribute();
			set_allAttributes([...allAttributes].concat(new_attribute));
			onClose_attributeCreator();
		};
	};

	return (
		<VStack width="90vw">
			<Text>TypeAdder</Text>
			<FormControl isRequired>
				<FormLabel>Name</FormLabel>
				<Input type='text' placeholder='Name' />
			</FormControl>
			<HStack minW='80%'>
				{/** The list of all allAttributes */}
				<FormControl width='30%'>
					<FormLabel>Select all Attributes</FormLabel>
					{allAttributes.map((attribute, index) => {
						return (
							<VStack key={attribute.attributeName} align="left">
								<Checkbox
									isChecked={AttributeManager.isAttributeNameIn(
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
				{/** The List of selected allAttributes */}
				<TableContainer width='70%'>
					<Table varient='simple'>
						<TableCaption placement='top' color='white'>Selected Attributes</TableCaption>
						<Thead>
							<Tr>
								<Th color='white'>Attribute Name</Th>
								<Th color='white'>Data Type</Th>
							</Tr>
						</Thead>
						<Tbody>
							{selectedAttributes.map((attribute) => {
								return (
									<Tr key={attribute.attributeName}>
										<Td>{attribute.attributeName}</Td>
										<Td>{attribute.attributeType}</Td>
									</Tr>
								);
							})}
						</Tbody>
					</Table>
				</TableContainer>
			</HStack>
			<Button onClick={open_AttributeCreator}>Add</Button>
			<Button>Save</Button>

			<Modal
				closeOnOverlayClick={false}
				isOpen={isOpen_attributeCreator}
				onClose={onClose_attributeCreator}
			>
				<ModalOverlay />
				<ModalContent color='black'>
					<ModalHeader>Create New Attribute</ModalHeader>
					<ModalCloseButton />
					<ModalBody>
						<FormControl isRequired isInvalid={new_attribute_errorMessage.attributeName !== ''}>
							<FormLabel>Attribute Name</FormLabel>
							<Input type='text'
								variant='outline'
								name='new_attributeName'
								placeholder='Name'
								onChange={(e) => {
									creationData.name = e.target.value;
									set_creationData(creationData);
								}}
							></Input>
							<FormErrorMessage>{new_attribute_errorMessage.attributeName}</FormErrorMessage>
						</FormControl>
						<FormControl isRequired>
							<FormLabel>Data Type</FormLabel>
							<Select
								name='new_attrType'
								onChange={(e) => {
									creationData.type = e.target.value;
									set_creationData(creationData);
									updateSelectedTypes();
								}}
							>
								{types.map((types) => {
									return (
										<option value={types} key={types}>{types}</option>
									);
								})}
							</Select>
						</FormControl>
						{/** Extra form for the num_lmt data type*/}
						{display_num_lmt &&
							<FormControl isRequired>
								<FormLabel>Number Range</FormLabel>
								<HStack>
									<input
										placeholder='Min'
										type='number'
										variant='outline'
										onChange={(e) => {
											creationData.min = e.target.value;
											set_creationData(creationData);
										}}
									></input>
									<input
										placeholder='Max'
										type='number'
										variant='outline'
										onChange={(e) => {
											creationData.max = e.target.value;
											set_creationData(creationData);
										}}
									></input>
								</HStack>
							</FormControl>
						}
					</ModalBody>
					<ModalFooter>
						<Button onClick={tryCreate_attribute}>Save</Button>
						<Button
							onClick={onClose_attributeCreator}>Cancel</Button>
					</ModalFooter>
				</ModalContent>
			</Modal>
		</VStack>
	);
};

export default TypeAdder;
