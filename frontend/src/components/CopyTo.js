import { Button, Heading, Modal, ModalBody, ModalCloseButton, ModalContent, ModalFooter, ModalHeader, ModalOverlay, useDisclosure } from '@chakra-ui/react';
import { useState } from 'react';
import { createTag, fetchTags } from '../api';
import SearchSelect from './SearchSelect';

const CopyTo = ({copyFunc}) => {
	const { isOpen, onOpen, onClose } = useDisclosure();
	const [tag, setTag] = useState(null);

	const handleCopy=()=>{
		if(tag){
			copyFunc(tag.id);
			onClose();
		}
	};
	return (
		<>
			<Button onClick={onOpen}>Copy To</Button>
			<Modal isOpen={isOpen} onClose={onClose}>
				<ModalOverlay />
				<ModalContent>
					<ModalHeader>Copy Selected Asset(s)</ModalHeader>
					<ModalCloseButton />
					<ModalBody>
						<Heading size="sm">Select a tag</Heading>
						<SearchSelect dataFunc={fetchTags} selectedValue={tag} setSelectedValue={setTag} createFunc={createTag}/>
					</ModalBody>
					<ModalFooter>
						<Button colorScheme='blue' mr={3} onClick={onClose}>Close</Button>
						<Button onClick={handleCopy}>Copy</Button>
					</ModalFooter>
				</ModalContent>
			</Modal> 
		</>);
};
 
export default CopyTo;