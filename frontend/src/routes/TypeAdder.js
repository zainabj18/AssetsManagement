
import {
	Button,
	FormControl, FormLabel, FormErrorMessage,
	Input,
	HStack, VStack,
	Text,
	useBoolean,
} from '@chakra-ui/react';
import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import TypeMethodManager from '../components/TypeMethodManager';
import { createType, fetchTypesList } from '../api';
import useAuth from '../hooks/useAuth';
import AttributeModal from '../components/AttributeModal';
import SelectedAttributesList from '../components/SelectedAttributesList';
import TypeSelection from '../components/TypeSelection';
import AttributeSelection from '../components/AttributeSelection';

const TypeAdder = () => {

	const { user } = useAuth();
	let navigate = useNavigate();

	useEffect(() => {
		if (user && user.userRole !== 'ADMIN') {
			navigate('../');
		}
	}, []);

	const [load_attribute_trigger, set_load_attribute_trigger] = useBoolean();
	const [typeName, set_typeName] = useState('');
	const [new_typeName_errorMessage, set_new_typeName_errorMessage] = useState('');
	const [selectedAttributes, set_selectedAttributes] = useState([]);
	const [selectedAttributes_hasError, set_selectedAttributes_hasError] = useState(false);
	const [selectedTypes, set_selectedTypes] = useState([]);

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

	const saveType = () => {
		fetchTypesList().then(data => {
			let typeNames = data.data;
			let name_already_exists = TypeMethodManager.isTypeNameIn(typeName, typeNames);
			let nameError = get_typeName_errorMessage(name_already_exists, typeName === '');
			set_new_typeName_errorMessage(nameError);

			let min1_selected_attribute = selectedAttributes.length > 0;
			set_selectedAttributes_hasError(!min1_selected_attribute);
			if (nameError === '' && min1_selected_attribute) {
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
		<VStack width="90vw" >

			<Text>TypeAdder</Text>
			<FormControl isRequired isInvalid={new_typeName_errorMessage !== ''}>
				<FormLabel>Name</FormLabel>
				<Input type='text'
					placeholder='Name'
					onChange={(e) => set_typeName(e.target.value)}
				/>
				<FormErrorMessage>{new_typeName_errorMessage}</FormErrorMessage>
			</FormControl>

			<HStack width='80vw' display={'flex'} flexDirection="row" alignItems={'flex-start'} justifyContent='flex-start' padding={5}>
				<AttributeSelection
					width='30%'
					selectedAttributes_state={selectedAttributes}
					set_selectedAttributes_state={set_selectedAttributes}
					load_attribute_trigger={load_attribute_trigger}
					isInvalid={selectedAttributes_hasError}
					isRequired='true'
				/>
				<SelectedAttributesList selectedAttributes_state={selectedAttributes} />
			</HStack>

			<TypeSelection
				selectedTypes_state={selectedTypes}
				set_selectedTypes_state={set_selectedTypes}
			/>

			<AttributeModal
				showModalButtonText="Add"
				load_allAttributes_setter={set_load_attribute_trigger}
			/>
			<Button onClick={saveType}>Save</Button>
		</VStack >
	);
};

export default TypeAdder;
