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
	Input,
	VStack,
	Fade
} from '@chakra-ui/react';
<<<<<<< HEAD
=======
import IndeterminateCheckbox from './IndeterminateCheckbox';
import GlobalFilter from './GlobalFilter';
 
>>>>>>> 9c001cf (Implemented global filter for project select)


function ProjectSelect({setSelectedProjects,projects}) {
	const { isOpen, onClose,onOpen, } = useDisclosure();
	const [selected,setSelected] = useState([]); 
	const [query,setQuery]= useState(''); 
	const [filters,setFilter]= useState({}); 
	const data = useMemo(
		() => 
			projects.map((value,index)=>{return {...value,rowID:index};}),
		[projects]);

	const columns = useMemo(
		() => {return {
			'id':{
				header: 'Project ID',
				Filter:p=>{return <Input type='number' onChange={(e)=>{setFilter((prev)=>({
					...prev,
					'id':e.target.value
				}));}} />;}
			},
			'name':{
				header: 'Project Name',
				Filter:p=>{return <Input onChange={(e)=>{setFilter((prev)=>({
					...prev,
					'name':e.target.value
				}));}} />;}
			},
			'description':{
				header: 'Project Decription',
				Filter:p=>{return <Input onChange={(e)=>{setFilter((prev)=>({
					...prev,
					'description':e.target.value
				}));}} />;}
			}
		};},[]
	);

<<<<<<< HEAD
	const filteredRows = useMemo(() => {
		if (!query && !filters) return data;
		let preFiltered=data.filter((obj)=>{
			for (const key of Object.keys(filters)) {

				if (!obj[key].toString().includes(filters[key])){
					return false;
				}
			}
			return true;});
		return preFiltered.filter((obj)=>Object.values(obj).toString().includes(query));
	  }, [filters,query, data]);
	
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
	const renderHeader=(key)=>{
		return (<VStack>
			<Th>{columns[key].header}</Th>
			{columns[key].hasOwnProperty('Filter')&& columns[key].Filter()}
		</VStack>);
		
	};
=======
	const {
		getTableProps,
		getTableBodyProps,
		headerGroups,
		rows,
		state,
		prepareRow,
		selectedFlatRows,
		setGlobalFilter,
	} = useTable(
		{
			columns,
			data,
		},
		useRowSelect,
		useGlobalFilter,
		hooks => {
			hooks.visibleColumns.push(columns => [
				{
					id: 'selection',
					Header: ({getToggleAllRowsSelectedProps}) => (
						<IndeterminateCheckbox {...getToggleAllRowsSelectedProps()}/>
					),
					Cell: ({row}) => (
						<IndeterminateCheckbox {...row.getToggleRowSelectedProps()}/>
					),
				},
				...columns,
			]);
		}
	);
    
 
	return (
		<TableContainer>
			 <GlobalFilter
				globalFilter={state.globalFilter}
				setGlobalFilter={setGlobalFilter}
			/>
			<Table {...getTableProps()} variant='striped'>
				<Thead>
					{headerGroups.map(headerGroup => (
						<Tr {...headerGroup.getHeaderGroupProps()}>
							{headerGroup.headers.map(column => (
								<Th
									{...column.getHeaderProps()}
								>
									{column.render('Header')}
								</Th>
							))}
						</Tr>
					))}
				</Thead>
				<Tbody {...getTableBodyProps()}>
					{rows.map(row => {
						prepareRow(row);
						return (
							<Tr {...row.getRowProps()}>
								{row.cells.map(cell => {
									return (
										<Td
											{...cell.getCellProps()}
										>
											{cell.render('Cell')}
										</Td>
									);
								})}
							</Tr>
						);
					})}
				</Tbody>
			</Table>
			<pre>
				<code>
					{console.log(selectedFlatRows.map(
						d=>d.original.id
>>>>>>> 9c001cf (Implemented global filter for project select)

	const onIntermediateCheckboxChange=(val)=>{
		
		if (val){
			setSelected([...Array(data.length).keys()]);
		}else{
			setSelected([]);
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
									<Th><Checkbox isChecked={data.length===selected.length}
										isIndeterminate={selected.length>0 && selected.length<data.length}
										onChange={(e)=>{onIntermediateCheckboxChange(e.target.checked);}}
									
									/></Th>
		  {Object.keys(columns).map(key => (
										<Th key={key}>
											{renderHeader(key)}	
										</Th>)
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