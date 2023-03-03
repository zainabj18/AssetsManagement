
import {
	Button,
	Checkbox,
	FormControl, FormLabel, FormErrorMessage,
	Input,
	HStack, VStack,
	Table, Thead, Tbody, Tr, Th, Td, TableContainer, TableCaption,
	Text,
	useBoolean,
	useDisclosure,
	Heading
} from '@chakra-ui/react';
import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import TypeAdderManager from '../components/TypeAdderManager';
import { fetchAllAttributes, createType, fetchTypesList } from '../api';
import useAuth from '../hooks/useAuth';
import AttributeModal from '../components/AttributeModal';

const TypeAdder = () => {

	const [trigger_load_attributes, setTrigger_load_attributes] = useBoolean();
	const [trigger_load_types, setTrigger_load_types] = useBoolean();
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

	useEffect(() => {
		async function load_allTypes() {
			let data = (await fetchTypesList(res => res.data)).data;
			console.log(data);
			set_allTypes(data);
		}
		load_allTypes();
	}, [trigger_load_types]);

	const [typeName, set_typeName] = useState('');
	const [new_typeName_errorMessage, set_new_typeName_errorMessage] = useState('');
	const [selectedAttributes, set_selectedAttributes] = useState([]);
	const [selectedAttributes_errorMessage, set_selectedAttributes_errorMessage] = useState('');
	const [selectedTypes, set_selectedTypes] = useState([]);
	const [allAttributes, set_allAttributes] = useState([]);
	const [allTypes, set_allTypes] = useState([]);

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

	const selectType = (id) => {
		selectedTypes.push(id);
		set_selectedTypes(selectedTypes);
	};

	const deselectType = (item, list) => {
		let index = list.indexOf(item);
		list.splice(index, 1);
		set_selectedTypes(list);
	};

	const ajustSelectedTypes = (checked, id) => {
		if (checked) {
			selectType(id);
		}
		if (!checked) {
			deselectType(id, selectedTypes);
		}
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
					metadata: selectedAttributes,
					dependsOn: selectedTypes
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
					<Heading placement='top' color='blue.900' size="md">Selected Attributes</Heading>
					<Table varient='simple'>

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

			<FormControl>
				<FormLabel>Depends On</FormLabel>
				{allTypes.map((allTypes) => {
					return (
						<Checkbox
							key={allTypes.type_id}
							onChange={(e) => {
								ajustSelectedTypes(e.target.checked, allTypes.type_id);
							}}
						>
							{allTypes.type_name}
						</Checkbox>
					);
				})}
			</FormControl>

			<AttributeModal
				showModalButtonText="Add"
				load_allAttributes_trigger={setTrigger_load_attributes}
			></AttributeModal>
			<Button onClick={saveType}>Save</Button>
		</VStack >
	);
};

export default TypeAdder;
