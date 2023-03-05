import {
	Heading, VStack, useBoolean, Button, Modal, ModalOverlay, ModalContent,
	ModalHeader, ModalCloseButton, ModalBody, ModalFooter,
	useDisclosure
} from '@chakra-ui/react';
import { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { createType, fetchAllAttributes, fetchType } from '../api';
import AttributeSelection from '../components/AttributeSelection';
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
	const [new_selectedAttributeIndexes ,set_new_selectedAttributeIndexes] = useState([]);

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

	const saveType = () => {
		// Backfill code
		fetchAllAttributes().then(data => {
			set_new_selectedAttributeIndexes(TypeMethodManager.getNewAttributeIndexes(selectedAttributes, type.metadata, data));
			onOpen();
		});
		// End of backfill code
		/* Lower code temp disabled for testing and implimenting backfill code
		if (!selectedAttributes_hasError && ) {
			createType({
				typeName: type.typeName,
				metadata: selectedAttributes,
				dependsOn: selectedTypes
			});
			navigate('/type');
		}*/
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
				<Heading>Can Backfill: {canBackfill.toString()}</Heading>
			</VStack>

			<Modal closeOnOverlayClick={false} isOpen={isOpen} onClose={onClose} variant="popup">
				<ModalOverlay />
				<ModalContent>
					<ModalHeader>Backfill Data</ModalHeader>
					<ModalBody>
						NewIndexesInAll: {new_selectedAttributeIndexes}
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