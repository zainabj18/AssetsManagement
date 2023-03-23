import React,{useEffect, useMemo,useState} from 'react';
import {
	Table,
	Thead,
	Tbody,
	Tr,
	Th,
	Td,
	TableContainer,
	Modal,
	ModalOverlay,
	ModalContent,
	ModalHeader,
	ModalFooter,
	ModalBody,
	ModalCloseButton,
	useDisclosure,
	Button,
	HStack,
	Box,
	Checkbox,
	Input,
	VStack,
} from '@chakra-ui/react';
import CustomTable from '../CustomTable';



function ProjectSelect({setProjectSelect,projectin}) {
	const { isOpen, onClose,onOpen, } = useDisclosure();
	const [selected,setSelected] = useState([]); 
	const columns = useMemo(
		() => {return {
			'projectID':{
				header: 'Project ID',
				canFilter:true
			},
			'projectName':{
				header: 'Project Name',
				canFilter:true
			},
			'projectDescription':{
				header: 'Project Decription',
				canFilter:true
			}
		};},[]
	);

	const save=()=>{
		console.log('Selected project',selected);
		setProjectSelect(selected);
		onClose();
	};

	useEffect(() => {
		let preSelected=[];
		for (let i = 0; i < projectin.length; i++) {
			let obj=projectin[i];
			if (obj.hasOwnProperty('isSelected')&&obj.isSelected){
				preSelected.push(i);
			}
		}
		setSelected(preSelected);
	}, [projectin]);
	

	return (<>
		<Button onClick={onOpen}>Select Projects</Button>
		<Modal isOpen={isOpen} onClose={onClose} size={'full'}>
			<ModalOverlay />
			<ModalContent>
				<ModalHeader>Project Select</ModalHeader>
				<ModalCloseButton />
				<ModalBody >
					{projectin && 
						<CustomTable rows={projectin} cols={columns}  setSelectedRows={setSelected} preSelIDs={selected}/>
					}
				</ModalBody>
				<ModalFooter>
					<HStack>
						<Button onClick={save}>Save</Button>
					</HStack>	
				</ModalFooter>
			</ModalContent>
			
		</Modal>
	</>
	);
}

export default ProjectSelect;