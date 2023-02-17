
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
	useBoolean,
	useDisclosure
} from '@chakra-ui/react';
import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import AttributeMaker from '../components/AttributeMaker';
import TypeAdderManager from '../components/TypeAdderManager';
import { fetchAllAttributes, createAttribute, createType, fetchTypesList } from '../api';
import useAuth from '../hooks/useAuth';

const TypeAdder = () => {

	const [trigger_load_attributes, setTrigger_load_attributes] = useBoolean();
	const { user } = useAuth();
	let navigate = useNavigate();

	useEffect(() => {
		if (user && user.userRole !== 'ADMIN') {
			navigate('../');
		}
		async function load_allAttributes() {
			let data = await fetchAllAttributes(res => res.data);
			set_allAttributes(data);
		}
		load_allAttributes();
	}, [trigger_load_attributes]);

	const {
		isOpen: isOpen_attributeCreator,
		onOpen: onOpen_attributeCreator,
		onClose: onClose_attributeCreator
	} = useDisclosure();

	const [types] = useState([
		'text', 'number', 'checkbox', 'datetime-local', 'num_lmt', 'options', 'list'
	]);

	const [typeName, set_typeName] = useState('');
	const [new_typeName_errorMessage, set_new_typeName_errorMessage] = useState('');
	const [selectedAttributes, set_selectedAttributes] = useState([]);
	const [selectedAttributes_errorMessage, set_selectedAttributes_errorMessage] = useState('');
	const [allAttributes, set_allAttributes] = useState([]);
	const [creationData, set_creationData] = useState(new AttributeMaker());
	const [new_attribute_errorMessage, set_new_attribute_errorMessage] = useState(AttributeMaker.get_message_noError());
	const [display_num_lmt, set_display_num_lmt] = useState(false);
	const [display_options, set_display_options] = useState(false);
	const [display_list, set_display_list] = useState(false);

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

	const updateSelectedTypes = (data = creationData) => {
		set_display_num_lmt(data.type === 'num_lmt');
		set_display_list(data.type === 'list');
		set_display_options(data.type === 'options');

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
			createAttribute(creationData.formAttribute()).then(_ => {
				setTrigger_load_attributes.toggle();
			});
			onClose_attributeCreator();
		};
	};

	const get_typeName_errorMessage = (name_already_exists, name_is_empty) => {
		let errorMessage = '';
		if (name_is_empty) {
			errorMessage = 'Please enter a name';
		}
		else if (name_already_exists) {
			errorMessage = 'Type name in use';
		}
		return errorMessage;
	};

	const get_selectedAttrs_errorMessage = (selected_count) => {
		let errorMessage = '';
		if (selected_count < 1) {
			errorMessage = 'At least 1 attribute must be selected';
		}
		return errorMessage;
	};

	const saveType = () => {
		fetchTypesList().then(data => {
			let typeNames = data.data;
			let name_already_exists = TypeAdderManager.isTypeNameIn(typeName, typeNames);
			let nameError = get_typeName_errorMessage(name_already_exists, typeName === '');
			let selectedError = get_selectedAttrs_errorMessage(selectedAttributes.length);
			set_new_typeName_errorMessage(nameError);
			set_selectedAttributes_errorMessage(selectedError);
			if (nameError + selectedError === '') {
				createType({
					typeName: typeName,
					metadata: selectedAttributes
				});
				navigate('/type');
			}
		});
	};

	return (
		<VStack width="90vw">
			<Text>TypeAdder</Text>
			<FormControl isRequired isInvalid={new_typeName_errorMessage !== ''}>
				<FormLabel>Name</FormLabel>
				<Input type='text'
					placeholder='Name'
					onChange={(e) => set_typeName(e.target.value)}
				/>
				<FormErrorMessage>{new_typeName_errorMessage}</FormErrorMessage>
			</FormControl>
			<HStack minW='80%'>

				{/** The list of all allAttributes */}
				<FormControl isRequired isInvalid={selectedAttributes_errorMessage !== ''} width='30%'>
					<FormLabel>Select Attributes</FormLabel>
					<FormErrorMessage>{selectedAttributes_errorMessage}</FormErrorMessage>
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
			<Button onClick={saveType}>Save</Button>

			<Modal
				closeOnOverlayClick={false}
				isOpen={isOpen_attributeCreator}
				onClose={onClose_attributeCreator}
			>
				<ModalOverlay />
				<ModalContent>
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
							</FormControl>}

						{/** Extra form for the options data type*/}
						{display_options && <FormControl isRequired>
							<FormLabel>Choices</FormLabel>
							<HStack>
								<input
									placeholder='options'
									type='text'
									variant='outline'
									onChange={(e) => {
										creationData.choices = e.target.value;
										set_creationData(creationData);
									}}
								></input>
								<Text>Multiselect</Text>
								<Checkbox onChange={(e) => {
									creationData.isMulti = e.target.checked;
									set_creationData(creationData);
								}} />
							</HStack>
						</FormControl>}

						{/** Extra form for the list data type*/}
						{display_list && <FormControl isRequired>
							<FormLabel>List Type</FormLabel>
							<Select onChange={(e) => {
								creationData.list_type = e.target.value;
								set_creationData(creationData);
							}}>
								<option>text</option>
								<option>email</option>
								<option>url</option>
							</Select>
						</FormControl>}

					</ModalBody>
					<ModalFooter>
						<Button onClick={tryCreate_attribute}>Save</Button>
						<Button onClick={onClose_attributeCreator}>Cancel</Button>
					</ModalFooter>
				</ModalContent>
			</Modal>
		</VStack>
	);
};

export default TypeAdder;
