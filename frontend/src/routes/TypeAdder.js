
import {
	Button,
	Checkbox,
	FormControl, FormLabel, FormErrorMessage,
	Input,
	HStack, VStack,
	Modal, ModalOverlay, ModalContent, ModalHeader, ModalCloseButton, ModalBody, ModalFooter,
	Table, Thead, Tbody, Tr, Th, Td, TableContainer, TableCaption,
	Text,
	useDisclosure
} from '@chakra-ui/react';
import React, { useState } from 'react';

const TypeAdder = () => {

	/** Class that represents an attribute */
	class Attr {
		constructor(attrName, attrType) {
			this.attrName = attrName;
			this.attrType = attrType;
		}
	}

	/** The selected attributes */
	const [selectedAttributes, setSelectedAttributes] = useState([
		new Attr('programming language', 'text')
	]);

	/** All attributes */
	const [attributes, setAttributes] = useState([
		new Attr('programming language', 'text'),
		new Attr('country of origin', 'text')
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

	/** Checks to see if the given name is also in the given list */
	const isAttrNameIn = (attrName, list) => {
		let i;
		for (i = 0; i < list.length; i++) {
			// eslint-disable-next-line
			if (list[i].attrName == attrName) {
				return true;
			}
		}
		return false;
	};

	/** States for the Modal */
	const { isOpen, onOpen, onClose } = useDisclosure();

	/** States and methods for the new attribute form input errors */
	const [new_attrName_errorMessage, set_new_attrName_errorMessage] = useState('');
	const [new_attrType_errorMessage, set_new_attrType_errorMessage] = useState('');
	const clearAttrErrors = () => {
		set_new_attrName_errorMessage('');
		set_new_attrType_errorMessage('');
	};

	/** Creates a new attribute if it passes the requirements
	 * other wise, it sets error messages */
	const createAttribute = () => {
		let inputs = document.getElementsByClassName('new_attrForm');
		let name = inputs[0].value;
		let type = inputs[1].value;
		let duplicate = isAttrNameIn(name, [...attributes]);
		let emptyName = name === '';
		let emptyType = type === '';

		if (emptyName) {
			set_new_attrName_errorMessage('Name is required');
		}
		else if (duplicate) {
			set_new_attrName_errorMessage('Name already in use');
		}
		else {
			set_new_attrName_errorMessage('');
		}

		if (emptyType) {
			set_new_attrType_errorMessage('Type is required');
		}
		else {
			set_new_attrType_errorMessage('');
		}

		let allGood = !emptyName && !emptyType && !duplicate;
		if (allGood) {
			setAttributes([...attributes, (new Attr(name, type))]);
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
							<VStack key={attr.attrName} align="left">
								<Checkbox
									isChecked={isAttrNameIn(attr.attrName, [...selectedAttributes])}
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
									<Tr key={attr.attrName}>
										<Td>{attr.attrName}</Td>
										<Td>{attr.attrType}</Td>
									</Tr>
								);
							})}
						</Tbody>
					</Table>
				</TableContainer>
			</HStack>
			<Button onClick={onOpen}>Add</Button>
			<Button>Save</Button>

			<Modal closeOnOverlayClick={false} isOpen={isOpen} onClose={() => { clearAttrErrors(); onClose(); }}>
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
								className='new_attrForm'
							></Input>
							<FormErrorMessage>{new_attrName_errorMessage}</FormErrorMessage>
						</FormControl>
						<FormControl isRequired isInvalid={new_attrType_errorMessage !== ''}>
							<FormLabel>Data Type</FormLabel>
							<Input type='text'
								variant='outline'
								name='new_attrType'
								className='new_attrForm'
							></Input>
							<FormErrorMessage>{new_attrType_errorMessage}</FormErrorMessage>
						</FormControl>
					</ModalBody>
					<ModalFooter>
						<Button onClick={createAttribute}>Save</Button>
						<Button onClick={() => { clearAttrErrors(); onClose(); }}>Cancel</Button>
					</ModalFooter>
				</ModalContent>
			</Modal>
		</VStack>
	);
};

export default TypeAdder;
