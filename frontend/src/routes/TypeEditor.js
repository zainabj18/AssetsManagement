import {
	Heading, VStack, useBoolean, Button, Modal, ModalOverlay, ModalContent,
	ModalHeader, ModalCloseButton, ModalBody, ModalFooter,
	useDisclosure,
	Input,
	Checkbox, Text, FormControl, FormLabel, FormErrorMessage
} from '@chakra-ui/react';
import { useEffect, useState, Fragment } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { createType, fetchAllAttributes, fetchType } from '../api';
import AttributeSelection from '../components/AttributeSelection';
import List from '../components/TypeEditorBackfill/List';
import Num_Lmt from '../components/TypeEditorBackfill/Num_Lmt';
import Options from '../components/TypeEditorBackfill/Options';
import TypeMethodManager from '../components/TypeMethodManager';
import TypeSelection from '../components/TypeSelection';

const TypeEditor = () => {
	let { id } = useParams();
	let navigate = useNavigate();

	const [toggle, set_toggle] = useBoolean();
	const { isOpen, onOpen, onClose } = useDisclosure();

	const [type, set_type] = useState([]);

	useEffect(() => {
		async function load_type() {
			let data = await fetchType(id, res => res.data);
			set_type(data);
			set_selectedAttributes(data.metadata);
			set_selectedTypes(data.dependsOn);
		}
		load_type();
	}, [toggle]);

	const [selectedTypes, set_selectedTypes] = useState([]);

	const [selectedAttributes, set_selectedAttributes] = useState([]);
	useEffect(() => {
		set_selectedAttributes_hasError(selectedAttributes.length < 1);
	}, [selectedAttributes]);
	const [new_selectedAttributes, set_new_selectedAttributes] = useState([]);
	const [new_attribute_data, set_new_attribute_data] = useState([]);
	const insertInto_new_attribute_data = (data, index) => {
		set_new_attribute_data(
			TypeMethodManager.insertInto(
				data, index, [...new_attribute_data]
			)
		);
	};
	const [new_attribute_data_errorMessages, set_new_attribute_data_errorMessages] = useState([]);

	const [load_attribute_trigger, set_load_attribute_trigger] = useBoolean();
	const [selectedAttributes_hasError, set_selectedAttributes_hasError] = useState(false);

	const [canBackfill, set_canBackfill] = useState(true);
	useEffect(() => {
		if (typeof type.dependsOn !== 'undefined' && typeof type.metadata !== 'undefined') {
			set_canBackfill(
				TypeMethodManager.doesContainAll(selectedTypes, type.dependsOn)
				&&
				selectedTypes.length === type.dependsOn.length
				&&
				TypeMethodManager.doesContainAll(
					TypeMethodManager.extractAttributeIds(selectedAttributes),
					TypeMethodManager.extractAttributeIds(type.metadata)
				)
			);
		}
	}, [selectedTypes, selectedAttributes]);
	const [wantsToBackfill, set_wantsToBackfill] = useState(false);

	const doBackFill = () => {
		fetchAllAttributes().then(allAttributes => {
			let new_selectedAttribiteIndexes = TypeMethodManager
				.getNewAttributeIndexes(selectedAttributes, type.metadata, allAttributes);
			let new_selectedAttributes = [];
			new_selectedAttribiteIndexes.forEach(index => {
				new_selectedAttributes.push(allAttributes[index]);
			});
			populate_new_attribute_data(new_selectedAttributes);
			set_new_selectedAttributes(new_selectedAttributes);
			let errorMessages = Array(new_selectedAttributes.length);
			errorMessages.fill('');;
			set_new_attribute_data_errorMessages(errorMessages);
			onOpen();
		});
	};

	const saveType = () => {
		if (!selectedAttributes_hasError) {
			createType({
				typeName: type.typeName,
				metadata: selectedAttributes,
				dependsOn: selectedTypes
			});
			navigate('/type');
		}
	};

	const populate_new_attribute_data = (new_selectedAttributes) => {
		let newList = [];
		new_selectedAttributes.forEach(attribute => {
			let type = attribute.attributeType;
			if (type === 'list') {
				newList.push([]);
			}
			if (type === 'num_lmt') {
				newList.push(attribute.validation.min);
			}
			if (type === 'options') {
				newList.push([]);
			}
			if (type === 'datetime-local') {
				newList.push('');
			}
			if (type === 'number') {
				newList.push(0);
			}
			if (type === 'checkbox') {
				newList.push(false);
			}
			if (type === 'text') {
				newList.push('');
			}
		});
		set_new_attribute_data(newList);
	};

	const default_backfillHandleChange = (value, index) => {
		insertInto_new_attribute_data(value, index);
	};

	const checkForError = (attributeIndex) => {
		if (attributeIndex >= new_attribute_data.length || attributeIndex >= new_selectedAttributes.length) {
			console.error('Lists not populated correctly.');
		}
		let data = new_attribute_data[attributeIndex];
		let attribute = new_selectedAttributes[attributeIndex];
		let type = attribute.attributeType;
		if (type === 'list') {
			if (data.length <= 0) {
				return 'Must contain at least 1 element';
			}
		}
		if (type === 'num_lmt') {
			if (!(attribute.validation.min <= data && data <= attribute.validation.max)) {
				return 'Number is outside of defined range';
			}
		}
		if (type === 'options') {
			if (data.length <= 0) {
				return 'Must contain at least 1 element';
			}
		}
		if (type === 'datetime-local') {
			if (data === '') {
				return 'Can not be left empty';
			}
		}
		if (type === 'number') {

		}
		if (type === 'checkbox') {

		}
		if (type === 'text') {
			if (data === '') {
				return 'Can not be left empty';
			}
		}
		return '';
	};

	const confirmBackfill = () => {
		let index = 0;
		let failed = false;
		let errorMessages = [];
		for (index = 0; index < new_attribute_data.length; index++) {
			let error = checkForError(index);
			errorMessages.push(error);
			if (error !== '') { failed = true; }
		}
		set_new_attribute_data_errorMessages(errorMessages);
		console.log(failed);
	};

	return (
		<>
			<VStack align='stetch'>
				<Heading as='h1' size='2xl'>Type: {type.typeName}</Heading>
				<Heading as='h2' size='1xl'>Version: {type.versionNumber}</Heading>
				<AttributeSelection
					selectedAttributes_state={selectedAttributes}
					set_selectedAttributes_state={set_selectedAttributes}
					load_attribute_trigger={load_attribute_trigger}
					isInvalid={selectedAttributes_hasError}
				/>
				<TypeSelection
					selectedTypes_state={selectedTypes}
					set_selectedTypes_state={set_selectedTypes}
					excludeIds={[type.typeId]}
				/>
				<Checkbox
					isDisabled={!canBackfill}
					isChecked={canBackfill && wantsToBackfill}
					onChange={(e) => set_wantsToBackfill(e.target.checked)}
				>Backfill Data</Checkbox>
				<Button onClick={saveType}>Save</Button>
				<Button onClick={doBackFill}>Testing: backfiller</Button>
				<Heading>Can: {canBackfill.toString()}</Heading>
				<Heading>Wants to: {wantsToBackfill.toString()}</Heading>
			</VStack>

			<Modal closeOnOverlayClick={false} isOpen={isOpen} onClose={onClose} variant="popup">
				<ModalOverlay />
				<ModalContent>
					<ModalHeader>Backfill Data</ModalHeader>
					<ModalCloseButton />
					<ModalBody>
						{new_selectedAttributes.length > 0 && new_selectedAttributes.map((attribute, index) => {
							let typeName = attribute.attributeType;
							if (typeName === 'list') {
								return (
									<Fragment key={index}>
										<List
											insertInto_new_attribute_data={insertInto_new_attribute_data}
											attribute={attribute}
											attributeIndex={index}
											isInvalid={new_attribute_data_errorMessages[index] !== ''}
											errorMessage={new_attribute_data_errorMessages[index]}
										/>
									</Fragment>
								);
							}
							if (typeName === 'num_lmt') {
								return (
									<Fragment key={index}>
										<Num_Lmt
											new_attribute_data={new_attribute_data}
											insertInto_new_attribute_data={insertInto_new_attribute_data}
											attribute={attribute}
											attributeIndex={index}
											isInvalid={new_attribute_data_errorMessages[index] !== ''}
											errorMessage={new_attribute_data_errorMessages[index]}
										/>
									</Fragment>
								);
							}
							if (typeName === 'options') {
								return (
									<Fragment key={index}>
										<Options
											new_attribute_data={new_attribute_data}
											insertInto_new_attribute_data={insertInto_new_attribute_data}
											attribute={attribute}
											attributeIndex={index}
											isInvalid={new_attribute_data_errorMessages[index] !== ''}
											errorMessage={new_attribute_data_errorMessages[index]}
										/>
									</Fragment>
								);
							}
							if (typeName === 'datetime-local') {
								return (
									<FormControl key={index} isInvalid={new_attribute_data_errorMessages[index] !== ''}>
										<FormLabel>{attribute.attributeName}</FormLabel>
										<FormErrorMessage>{new_attribute_data_errorMessages[index]}</FormErrorMessage>
										<Input
											type='datetime-local'
											onChange={(e) => default_backfillHandleChange(e.target.value, index)}
										/>
									</FormControl>
								);
							}
							if (typeName === 'number') {
								return (
									<FormControl key={index} isInvalid={new_attribute_data_errorMessages[index] !== ''}>
										<FormLabel>{attribute.attributeName}</FormLabel>
										<FormErrorMessage>{new_attribute_data_errorMessages[index]}</FormErrorMessage>
										<Input
											type='number'
											defaultValue={new_attribute_data[index]}
											onChange={(e) => default_backfillHandleChange(e.target.value, index)}
										/>
									</FormControl>
								);
							}
							if (typeName === 'checkbox') {
								return (
									<FormControl key={index} isInvalid={new_attribute_data_errorMessages[index] !== ''}>
										<FormLabel>{attribute.attributeName}</FormLabel>
										<FormErrorMessage>{new_attribute_data_errorMessages[index]}</FormErrorMessage>
										<Checkbox
											type='checkbox'
											onChange={(e) => default_backfillHandleChange(e.target.checked, index)}
										>Select</Checkbox>
									</FormControl>
								);
							}
							if (typeName === 'text') {
								return (
									<FormControl key={index} isInvalid={new_attribute_data_errorMessages[index] !== ''}>
										<FormLabel>{attribute.attributeName}</FormLabel>
										<FormErrorMessage>{new_attribute_data_errorMessages[index]}</FormErrorMessage>
										<Input
											type='text'
											placeholder='Enter Text'
											onChange={(e) => default_backfillHandleChange(e.target.value, index)}
										/>
									</FormControl>
								);
							}
						})}
					</ModalBody>
					<ModalFooter>
						<Button onClick={confirmBackfill}>Confirm</Button>
						<Button onClick={onClose}>Cancel</Button>
					</ModalFooter>
				</ModalContent>
			</Modal>
		</>
	);
};

export default TypeEditor;