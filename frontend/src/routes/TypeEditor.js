import {
	Heading, VStack, useBoolean, Button, Modal, ModalOverlay, ModalContent,
	ModalHeader, ModalCloseButton, ModalBody, ModalFooter,
	useDisclosure,
	Input,
	Checkbox, Text
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
				<Button onClick={saveType}>Save</Button>
				<Button onClick={doBackFill}>Testing: backfiller</Button>
			</VStack>

			<Modal closeOnOverlayClick={false} isOpen={isOpen} onClose={onClose} variant="popup">
				<ModalOverlay />
				<ModalContent>
					<ModalHeader>Backfill Data</ModalHeader>
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
										/>
									</Fragment>
								);
							}
							if (typeName === 'datetime-local') {
								return (
									<Fragment key={index}>
										<Text>{attribute.attributeName}</Text>
										<Input
											type='datetime-local'
											onChange={(e) => default_backfillHandleChange(e.target.value, index)}
										/>
									</Fragment>
								);
							}
							if (typeName === 'number') {
								return (
									<Fragment key={index}>
										<Text>{attribute.attributeName}</Text>
										<Input
											type='number'
											defaultValue={new_attribute_data[index]}
											onChange={(e) => default_backfillHandleChange(e.target.value, index)}
										/>
									</Fragment>
								);
							}
							if (typeName === 'checkbox') {
								return (
									<Fragment key={index}>
										<Text>{attribute.attributeName}</Text>
										<Checkbox
											type='checkbox'
											onChange={(e) => default_backfillHandleChange(e.target.checked, index)}
										>Select</Checkbox>
									</Fragment>
								);
							}
							if (typeName === 'text') {
								return (
									<Fragment key={index}>
										<Text>{attribute.attributeName}</Text>
										<Input
											type='text'
											placeholder='Enter Text'
											onChange={(e) => default_backfillHandleChange(e.target.value, index)}
										/>
									</Fragment>
								);
							}
						})}
					</ModalBody>
					<ModalFooter>
						<Button>Confirm</Button>
						<Button onClick={onClose}>Cancel</Button>
					</ModalFooter>
				</ModalContent>
			</Modal>
		</>
	);
};

export default TypeEditor;