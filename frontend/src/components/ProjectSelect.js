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
	Checkbox,
	Input
} from '@chakra-ui/react';


function ProjectSelect({setSelectedProjects,projects}) {
	const { isOpen, onClose,onOpen, } = useDisclosure();
	const [selected,setSelected] = useState([]); 
	const [query,setQuery]= useState(''); 
	const data = useMemo(
		() => 
			projects.map((value,index)=>{return {...value,rowID:index};}),
		[projects]);
	//	
	const columns = useMemo(
		() => {return {
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

	const filteredRows = useMemo(() => {
		console.log(data);
		if (!query) return data;
		return data.filter((obj)=>Object.values(obj).toString().includes(query));
	  }, [query, data]);
	
	const save=()=>{
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
	const renderCell=(key,rowID,value)=>{
		if (columns[key].hasOwnProperty('Cell')){
			return columns[key].Cell(rowID,value);
		}else{
			return <Box>{value}</Box>;
		}
	};

	useEffect(() => {
		let preSelected=[];
		let projects=[];
		for (let i = 0; i < data.length; i++) {
			let obj=data[i];
			if (obj.hasOwnProperty('isSelected')&obj.isSelected){
				preSelected.push(i);
				projects.push(obj);
			}
		}
		setSelected(preSelected);
		setSelectedProjects(projects);
	}, []);
	

	
	return (<>
		<Button onClick={onOpen}>Select Projects</Button>
		<Modal isOpen={isOpen} onClose={onClose} size={'full'}>
			<ModalOverlay />
			<ModalContent>
				<ModalHeader>Project Select</ModalHeader>
				<ModalCloseButton />
				<ModalBody >
					{projects && <TableContainer>
						<Input onChange={(e)=>{setQuery(e.target.value);}}/>
						<Table variant='stripped'>
		  <Thead>
								<Tr key={'header'}>
									<Th>Select</Th>
		  {Object.keys(columns).map(key => (
										<Th key={key}>{columns[key].header}</Th>)
		  )}
		  </Tr>
		  </Thead>
		  <Tbody>
		  {filteredRows.map((row,index)=> (
									<Tr key={index}>
										<Td><Checkbox defaultChecked={selected.includes(row.rowID)} isChecked={selected.includes(row.rowID)} onChange={(e) => handleCheck(row.rowID,e.target.checked)} /></Td>
										{Object.keys(columns).map((key)=>{

	 return <Td key={index+key}>{renderCell(key,row.rowID,row[key])}</Td>;
										})}</Tr>)
								)}
		 
		  </Tbody>
						</Table>
					</TableContainer>}
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