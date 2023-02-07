import React,{useEffect, useMemo,useState} from 'react';
import { useTable,useRowSelect,useGlobalFilter } from 'react-table';

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
	Checkbox
} from '@chakra-ui/react';


function ProjectSelect({setSelectedProjects,projects}) {
	const { isOpen, onClose,onOpen } = useDisclosure();
	const [selected,setSelected] = useState([]); 
	const data = React.useMemo(
		() => 
			[...projects,{'id': 2, 'name': 'mike', 'description': 'mike','isSelected':true}],
		[projects]);

	const columns = useMemo(
		() => {return {
			'isSelected':{
				header: 'Selection'
			},
			'id':{
				header: 'Project ID'
			},
			'name':{
				header: 'Project Name',
			},
			'description':{
				header: 'Project Decription'
			}
		};},[]
	);
	const addProjects=()=>{
		let selectedProjects=selected.map(
			(rowID)=>{return data[rowID];});
		setSelectedProjects(selectedProjects);
		onClose();
	};

	const handleCheck=(rowID,val)=>{
		if (val){
			if (!selected.includes(rowID)){
				setSelected((prev)=>{return  [...prev,rowID];});
			}
		}else {
			let newSelected=selected.filter((id) => id !==rowID);
			setSelected(newSelected);
		}	
	};
	const renderCell=(key,value)=>{
		if (columns[key].hasOwnProperty('Cell')){
			return columns[key].Cell(value);
		}else{
			return <Box>{value}</Box>;
		}
	};
	return (<>
		<Button onClick={onOpen}>Select Projects</Button>
		<Modal isOpen={isOpen} onClose={onClose} size={'full'}>
			<ModalOverlay />
			<ModalContent>
				<ModalHeader>Project Select</ModalHeader>
				<ModalCloseButton />
				<ModalBody >
					{projects && <TableContainer>
						<Table variant='simple'>
		  <Thead>
								<Tr key={'header'}>
		  {Object.keys(columns).map(key => (
										<Th key={key}>{columns[key].header}</Th>)
		  )}
		  </Tr>
		  </Thead>
		  <Tbody>
		  {data.map((row,index)=> (

									<Tr key={index}>
										<Td><Checkbox defaultChecked={selected.includes(index)} onChange={(e) => handleCheck(index,e.target.checked)}/></Td>
										{Object.keys(row).map((key)=>{

						
	 return <Td key={index+key}>{renderCell(key,row[key])}</Td>;
										})}</Tr>)
								)}
		 
		  </Tbody>
						</Table>
					</TableContainer>}
				</ModalBody>

				<ModalFooter>
					<HStack>
						<Button onClick={addProjects}>Save</Button>
					</HStack>	
				</ModalFooter>
			</ModalContent>
			
		</Modal>
	</>
	);
}

export default ProjectSelect;