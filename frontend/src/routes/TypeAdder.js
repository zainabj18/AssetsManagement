
import {
	Button,
	Checkbox,
	FormControl, FormLabel, FormErrorMessage,
	Input,
	HStack, VStack,
	Text,
	useBoolean,
} from '@chakra-ui/react';
import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import TypeAdderManager from '../components/TypeAdderManager';
import { fetchAllAttributes, createType, fetchTypesList } from '../api';
import useAuth from '../hooks/useAuth';
import AttributeModal from '../components/AttributeModal';
import SelectedAttributesList from '../components/SelectedAttributesList';
import DependsOnMenu from '../components/DependsOnMenu';

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

	const [typeName, set_typeName] = useState('');
	const [new_typeName_errorMessage, set_new_typeName_errorMessage] = useState('');
	const [selectedAttributes, set_selectedAttributes] = useState([]);
	const [selectedAttributes_errorMessage, set_selectedAttributes_errorMessage] = useState('');
	const [selectedTypes, set_selectedTypes] = useState([]);
	const [allAttributes, set_allAttributes] = useState([]);

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

				<SelectedAttributesList selectedAttributes_state={selectedAttributes} />

			</HStack>

			<DependsOnMenu set_selectedTypes_state={set_selectedTypes}/>

			<AttributeModal
				showModalButtonText="Add"
				load_allAttributes_setter={setTrigger_load_attributes}
			/>
			<Button onClick={saveType}>Save</Button>
		</VStack >
	);
};

export default TypeAdder;
