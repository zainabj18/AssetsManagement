import {Button, Drawer, DrawerBody, DrawerCloseButton, DrawerContent, DrawerFooter, DrawerHeader, DrawerOverlay, Input, useDisclosure} from '@chakra-ui/react';
import { useState } from 'react';
import { createTag } from '../api';
const NewTag = () => {
	const [name, setName] = useState('');
	const { isOpen, onOpen, onClose } = useDisclosure();

	const saveTag = (e) => {
		if (name){
			createTag(name);
			onClose();
		}
	};

	return (  <>
		<Button onClick={onOpen}>Create</Button>
		<Drawer isOpen={isOpen} onClose={onClose}>
			<DrawerOverlay />
			<DrawerContent>
				<DrawerCloseButton />
				<DrawerHeader>Create new tag</DrawerHeader>
				<DrawerBody>
					<Input value={name} onChange={(e)=>{setName(e.target.value);}} placeholder='Enter tag name here...' />
				</DrawerBody>
				<DrawerFooter>
					<Button onClick={saveTag}>
                Save
					</Button>
				</DrawerFooter>
			</DrawerContent>
		</Drawer>
	</> );
};
 
export default NewTag;