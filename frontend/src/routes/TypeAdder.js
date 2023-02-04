
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
import React, { useState } from 'react';

const TypeAdder = () => {

	const formAttribute = (name, type) => {
		return {attributeName: name, attributeType: type};
	};

	/** The selected attributes */
	const [selectedAttributes, setSelectedAttributes] = useState([ ]);

	/** All attributes */
	const [attributes, setAttributes] = useState([
		/** Dummy Data */
		{
			attributeName: 'programming Language(s)',
			attributeType: 'text',
		},
		{
			attributeName: 'public',
			attributeType: 'checkbox',
		},
		{
			attributeName: 'no. of issues',
			attributeType: 'number',
		},
		{
			attributeName: 'built on',
			attributeType: 'datetime-local',
		},
		{
			attributeName: 'version',
			attributeType: 'text',
		},
		{
			attributeName: 'stars',
			attributeType: 'num_lmt',
			validation: {
				min: 1,
				max: 5
			}
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
			attributeName: 'authors',
			attributeType: 'list',
			validation: {
				type: 'text'
			}
		},
		{
			attributeName: 'authors_emails',
			attributeType: 'list',
			validation: {
				type: 'email'
			}
		},
		{
			attributeName: 'authors_emails_domain',
			attributeType: 'list',
			validation: {
				type: 'url'
			}
		},
		{
			attributeName: 'platform',
			attributeType: 'text',
		},
		{
			attributeName: 'private',
			attributeType: 'checkbox',
		},
		{
			attributeName: 'last modified',
			attributeType: 'datetime-local',
		},
		{
			attributeName: 'description',
			attributeType: 'text',
		},
		{
			attributeName: 'fileSize(kb)',
			attributeType: 'number',
		}
		/** End of Dummy Data */
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
		let list = [...selectedAttributes];
		list.push(data[attrindex]);
		setSelectedAttributes(sortAttrs(list));
	};

	/** Removes an attribute from the selected attributes */
	const removeAttr = (attr) => {
		let selectedData = [...selectedAttributes];
		let index = selectedData.indexOf(attr);
		selectedData.splice(index, 1);
		setSelectedAttributes(selectedData);
	};

	/** Checks to see if the given name is also in the given list */
	const isAttrNameIn = (attrName, list) => {
		let i;
		for (i = 0; i < list.length; i++) {
			// eslint-disable-next-line
			if (list[i].attributeName == attrName) {
				return true;
			}
		}
		return false;
	};

	/** An insersion sort for attributes */
	const sortAttrs = (attrs) => {
		let size = attrs.length;
		let index;
		for (index = 1; index < size; index++) {
			let pos  = index - 1;
			let currentItem = attrs[index];
			while (pos >= 0 && currentItem.attributeName < attrs[pos].attributeName) {
				let temp = attrs[pos];
				attrs[pos] = attrs[pos + 1];
				attrs[pos + 1] = temp;
				pos -= 1;
			}
		}
		return attrs;
	};

	/** States for the Modal */
	const { isOpen, onOpen, onClose } = useDisclosure();

	/** Type options
	 References https://developer.mozilla.org/en-US/docs/Web/HTML/Element/Input*/
	const [types] = useState([
		'text', 'number', 'checkbox', 'email', 'date', 'time', 'week', 'month'
	]);

	/** States and methods for the new attribute form*/
	const [new_attrForm] = useState([
		new Map([['name', ''], ['type', '']])
	]);
	const update_new_attrForm = (key, data) => {
		[...new_attrForm][0].set(key, data);
	};
	const [new_attrName_errorMessage, set_new_attrName_errorMessage] = useState('');

	/** Creates a new attribute if it passes the requirements
	 * otherwise, it sets error messages */
	const createAttribute = () => {
		let name = [...new_attrForm][0].get('name');
		let type = [...new_attrForm][0].get('type');
		let duplicate = isAttrNameIn(name, [...attributes]);
		let emptyName = name === '';

		if (emptyName) {
			set_new_attrName_errorMessage('Name is required');
		}
		else if (duplicate) {
			set_new_attrName_errorMessage('Name already in use');
		}
		else {
			set_new_attrName_errorMessage('');
		}

		let allGood = !emptyName && !duplicate;
		if (allGood) {
			setAttributes([...attributes, formAttribute(name, type)]);
			onClose();
		}
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
					<FormLabel>Select attributes</FormLabel>
					{attributes.map((attr, index) => {
						return (
							<VStack key={attr.attributeName} align="left">
								<Checkbox
									isChecked={isAttrNameIn(attr.attributeName, [...selectedAttributes])}
									value={attr.attributeName}
									onChange={(e) => ajustSelectedAttributes(e.target.checked, index)}
								> {attr.attributeName}
								</Checkbox>
							</VStack>
						);
					})}
				</FormControl>
				{/** The List of selected attributes */}
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
							{selectedAttributes.map((attr) => {
								return (
									<Tr key={attr.attributeName}>
										<Td>{attr.attributeName}</Td>
										<Td>{attr.attributeType}</Td>
									</Tr>
								);
							})}
						</Tbody>
					</Table>
				</TableContainer>
			</HStack>
			<Button onClick={onOpen}>Add</Button>
			<Button>Save</Button>

			<Modal closeOnOverlayClick={false} isOpen={isOpen} onClose={() => { set_new_attrName_errorMessage(''); onClose(); }}>
				<ModalOverlay />
				<ModalContent color='black'>
					<ModalHeader>Create New Attribute</ModalHeader>
					<ModalCloseButton />
					<ModalBody>
						<FormControl isRequired isInvalid={new_attrName_errorMessage !== ''}>
							<FormLabel>Attribute Name</FormLabel>
							<Input type='text'
								variant='outline'
								name='new_attrName'
								placeholder='Name'
								onChange={(e) => update_new_attrForm('name', e.target.value)}
							></Input>
							<FormErrorMessage>{new_attrName_errorMessage}</FormErrorMessage>
						</FormControl>
						<FormControl isRequired>
							<FormLabel>Data Type</FormLabel>
							<Select
								name='new_attrType'
								onLoad={update_new_attrForm('type', types[0])}
								onChange={(e) => update_new_attrForm('type', e.target.value)}
							>
								{types.map((types) => {
									return (
										<option value={types} key={types}>{types}</option>
									);
								})}
							</Select>
						</FormControl>
					</ModalBody>
					<ModalFooter>
						<Button onClick={createAttribute}>Save</Button>
						<Button onClick={() => { set_new_attrName_errorMessage(''); onClose(); }}>Cancel</Button>
					</ModalFooter>
				</ModalContent>
			</Modal>
		</VStack>
	);
};

export default TypeAdder;
