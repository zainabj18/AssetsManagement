import { Button, Heading, Modal, ModalBody, ModalCloseButton, ModalContent, ModalFooter, ModalHeader, ModalOverlay, useDisclosure } from '@chakra-ui/react';
import { useState } from 'react';
import { createTag, fetchTags } from '../api';
import SearchSelect from './asset/formfields/SearchSelect';

const OperationTo = ({actionFunc,actionName}) => {
	const { isOpen, onOpen, onClose } = useDisclosure();
	const [tag, setTag] = useState(null);

	const handleCopy=()=>{
		if(tag){
			actionFunc(tag.id);
			onClose();
		}
	};
	return (
		<>
			<Button onClick={onOpen}>{actionName} To</Button>
			<Modal isOpen={isOpen} onClose={onClose} variant="popup">
				<ModalOverlay />
				<ModalContent bg="white">
					<ModalHeader>{actionName} Selected Asset(s)</ModalHeader>
					<ModalCloseButton />
					<ModalBody>
						<Heading size="sm">Select a tag:</Heading>
						<SearchSelect dataFunc={fetchTags} selectedValue={tag} setSelectedValue={setTag} createFunc={createTag}/>
					</ModalBody>
					<ModalFooter>
						<Button colorScheme='blue' mr={3} onClick={onClose}>Close</Button>
						<Button onClick={handleCopy}>{actionName}</Button>
					</ModalFooter>
				</ModalContent>
			</Modal> 
		</>);
};
 
export default OperationTo;