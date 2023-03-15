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
			'projectID':{
				header: 'Project ID',
				Filter:p=>{return <Input  bg="white" sx={{border:"1px solid black"}}  type='number' onChange={(e)=>{setFilter((prev)=>({
					...prev,
					'id':e.target.value
				}));}} />;}
			},
			'projectName':{
				header: 'Project Name',
				Filter:p=>{return <Input  bg="white" sx={{border:"1px solid black"}}  onChange={(e)=>{setFilter((prev)=>({
					...prev,
					'name':e.target.value
				}));}} />;}
			},
			'projectDescription':{
				header: 'Project Decription',
				Filter:p=>{return <Input bg="white" sx={{border:"1px solid black"}} onChange={(e)=>{setFilter((prev)=>({
					...prev,
					'description':e.target.value
				}));}} />;}
			}
		};},[]
	);

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
			<Th bg={'white'}>{columns[key].header}</Th>
			{columns[key].hasOwnProperty('Filter')&& columns[key].Filter()}
		</VStack>);
		
	};

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
		console.log(data,preSelected,'I am in projects');
		setSelected(preSelected);
		setSelectedProjects(projects);
	}, [projects]);
	

	
	return (<Box >
		<Button onClick={onOpen}>Select Projects</Button>
		<Modal isOpen={isOpen} onClose={onClose} size={'full'}>
			<ModalOverlay />
			<ModalContent  background='#e3e3e3'>
				<ModalHeader textAlign="center" paddingY={5}>Project Select</ModalHeader>
				<ModalCloseButton />
				<ModalBody >
					{projects && <TableContainer>
						<Input onChange={(e)=>{setQuery(e.target.value);}} background="white" paddingY="5px" placeholder='Enter here...'/>
						<Table variant='stripped'>
		  <Thead alignContent={'center'} alignItems="center" width="90vw" rounded={10} bg="#ed7966">
								<Tr key={'header'} border={"1px solid"} background="#ed7966" marginY={5}> 
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
		  <Tbody bg={'white'} sx={{
		tr: {
			border:'none',
			'&:nth-of-type(odd)': {
				td:{
					bg:'white',
					color:'blue.900'
				}
			},
			'&:nth-of-type(even)': {
				td: {
					bg:'blue.100',
					color:'blue.900'
				}
			}
		
	}}}>
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
	</Box>
	);
}

export default ProjectSelect;