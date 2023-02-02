
import {
	Button,
	Checkbox,
	FormControl, FormLabel,
	Input,
	HStack, VStack,
	Modal, ModalOverlay, ModalContent, ModalHeader, ModalCloseButton, ModalBody, ModalFooter,
	Table, Thead, Tbody, Tr, Th, Td, TableContainer, TableCaption,
	Text,
	useDisclosure
} from '@chakra-ui/react';
import React, { useState } from 'react';

const TypeAdder = () => {

	class Attr {
		constructor(priKey, attrName, attrType) {
			this.priKey = priKey;
			this.attrName = attrName;
			this.attrType = attrType;
		}
	}

	/** The selected attributes */
	const [selectedAttributes, setSelectedAttributes] = useState([
		new Attr('0', 'programming language', 'text')
	]);

	/** All attributes */
	const [attributes, setAttributes] = useState([
		new Attr('0', 'programming language', 'text'),
		new Attr('1', 'country of origin', 'text')
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
	const sameChecked = (priKey) => {
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

	const { isOpen, onOpen, onClose } = useDisclosure();

	const createAttribute = () => {
		let inputs = document.getElementsByClassName('new_attrForm');
		setAttributes([...attributes , (new Attr('2',inputs[0].value, inputs[1].value))]);
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
							<VStack key={attr.priKey} align="left">
								<Checkbox
									isChecked={sameChecked(attr.priKey)}
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
			<Button onClick={onOpen}>Add</Button>
			<Button>Save</Button>

			<Modal closeOnOverlayClick={false} isOpen={isOpen} onClose={onClose}>
				<ModalOverlay />
				<ModalContent color='black'>
					<ModalHeader>Create New Attribute</ModalHeader>
					<ModalCloseButton />
					<ModalBody>
						<FormControl>
							<FormLabel>Attribute Name</FormLabel>
							<Input type='text'
								variant='outline'
								name='new_attrName'
								className='new_attrForm'
							></Input>
						</FormControl>
						<FormControl>
							<FormLabel>Data Type</FormLabel>
							<Input type='text'
								variant='outline'
								name='new_attrType'
								className='new_attrForm'
							></Input>
						</FormControl>
					</ModalBody>
					<ModalFooter>
						<Button onClick={createAttribute}>Save</Button>
						<Button onClick={onClose}>Cancel</Button>
					</ModalFooter>
				</ModalContent>
			</Modal>
		</VStack>
	);
};

export default TypeAdder;
