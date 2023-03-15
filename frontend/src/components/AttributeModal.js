import {
	Button,
	Checkbox,
	FormControl, FormLabel, FormErrorMessage,
	Input,
	HStack,
	Modal, ModalOverlay, ModalContent, ModalHeader, ModalCloseButton, ModalBody, ModalFooter,
	Select,
	Text,
	useDisclosure,
} from '@chakra-ui/react';
import React, { useState } from 'react';
import AttributeMaker from '../components/AttributeMaker';
import { createAttribute, isAttributeNameIn } from '../api';

const AttributeModal = ({ showModalButtonText, load_allAttributes_setter }) => {

	const [types] = useState([
		'text', 'number', 'checkbox', 'datetime-local', 'num_lmt', 'options', 'list'
	]);
	const [list_types] = useState([
		'text', 'email', 'url'
	]);

	const { isOpen, onOpen, onClose } = useDisclosure();

	const [creationData, set_creationData] = useState(new AttributeMaker());

	const [new_attribute_errorMessage, set_new_attribute_errorMessage] = useState(AttributeMaker.get_message_noError());
	const [display_num_lmt, set_display_num_lmt] = useState(false);
	const [display_options, set_display_options] = useState(false);
	const [display_list, set_display_list] = useState(false);

	const open_AttributeCreator = () => {
		let new_data = new AttributeMaker();
		new_data.type = types[0];
		new_data.list_type = list_types[0];
		update_selected_dataTypes(new_data);
		set_new_attribute_errorMessage(AttributeMaker.get_message_noError());
		set_creationData(new_data);
		onOpen();
	};

	const update_selected_dataTypes = (data = creationData) => {
		set_display_num_lmt(data.type === 'num_lmt');
		set_display_list(data.type === 'list');
		set_display_options(data.type === 'options');
	};

	const tryCreate_attribute = () => {
		isAttributeNameIn({ name: creationData.name }).then(data => {
			let nameExists = data.data;
			let errorMessage = creationData.checkForErrors(nameExists);
			set_new_attribute_errorMessage(errorMessage);
			if (JSON.stringify(errorMessage) === JSON.stringify(AttributeMaker.get_message_noError())) {
				createAttribute(creationData.formAttribute()).then(_ => {
					load_allAttributes_setter.toggle();
					onClose();
				});
			};
		});
	};

	return (
		<>
			<Button onClick={open_AttributeCreator}>{showModalButtonText}</Button>
			<Modal
				closeOnOverlayClick={false}
				isOpen={isOpen}
				onClose={onClose}
				variant="popup"
			>
				<ModalOverlay />
				<ModalContent bg="white">
					<ModalHeader>Create New Attribute</ModalHeader>
					<ModalCloseButton />
					<ModalBody>
						<FormControl isRequired isInvalid={new_attribute_errorMessage.attributeName !== ''}>
							<FormLabel>Attribute Name</FormLabel>
							<Input type='text'
								name='new_attributeName'
								placeholder='Name'
								bg={'white'}
								border={'1px solid black'}
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
									update_selected_dataTypes();
								}}
							>
								{types.map((types) => {
									return (
										<option value={types} key={types}>{types}</option>
									);
								})}
							</Select>
						</FormControl>
						<FormControl>
							<Checkbox
								onChange={(e) => {
									creationData.isOptional = e.target.checked;
									set_creationData(creationData);
								}}
							>
								Optional
							</Checkbox>
						</FormControl>

						{/** Extra form for the num_lmt data type*/}
						{display_num_lmt &&
							<FormControl isRequired isInvalid={new_attribute_errorMessage.num_lmt !== ''}>
								<FormLabel>Number Range</FormLabel>
								<HStack>
									<Input
										placeholder='Min'
										type='number'
										bg={'white'}
										border={'1px solid black'}
										onChange={(e) => {
											creationData.min = e.target.value;
											set_creationData(creationData);
										}}
									></Input>
									<Input
										placeholder='Max'
										type='number'
										bg={'white'}
										border={'1px solid black'}
										onChange={(e) => {
											creationData.max = e.target.value;
											set_creationData(creationData);
										}}
									></Input>
								</HStack>
								<FormErrorMessage>{new_attribute_errorMessage.num_lmt}</FormErrorMessage>
							</FormControl>
						}

						{/** Extra form for the options data type*/}
						{display_options &&
							<FormControl>
								<FormLabel>Choices</FormLabel>
								<HStack>
									<FormControl isRequired isInvalid={new_attribute_errorMessage.options !== ''}>
										<Input
											placeholder='options'
											type='text'
											bg={'white'}
											border={'1px solid black'}

											onChange={(e) => {
												creationData.choices = e.target.value;
												set_creationData(creationData);
											}}
										></Input>
										<FormErrorMessage>{new_attribute_errorMessage.options}</FormErrorMessage>
									</FormControl>
									<Text>Multiselect</Text>
									<Checkbox onChange={(e) => {
										creationData.isMulti = e.target.checked;
										set_creationData(creationData);
									}} />
								</HStack>
							</FormControl>
						}

						{/** Extra form for the list data type*/}
						{display_list &&
							<FormControl isRequired>
								<FormLabel>List Type</FormLabel>
								<Select onChange={(e) => {
									creationData.list_type = e.target.value;
									set_creationData(creationData);
								}}>
									{list_types.map((list_types) => {
										return (<option value={list_types} key={list_types}>{list_types}</option>
										);
									})}
								</Select>
							</FormControl>}

					</ModalBody>
					<ModalFooter display={'flex'} justifyContent="space-between" marginX={3}>
						<Button onClick={tryCreate_attribute}>Save</Button>
						<Button onClick={onClose}>Cancel</Button>
					</ModalFooter>
				</ModalContent>
			</Modal>
		</>
	);
};

export default AttributeModal;