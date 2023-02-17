import React,{useEffect, useMemo,useState} from 'react';
import {
	Table,
	Thead,
	Tbody,
	Tr,
	Th,
	Td,
	TableContainer,
	Box,
	Checkbox,
	Input,
	VStack,
	Alert,
	AlertIcon
} from '@chakra-ui/react';



function CustomTable({setSelectedRows,rows,cols}) {
	const [selected,setSelected] = useState([]); 
	const [query,setQuery]= useState(''); 
	const [filters,setFilter]= useState({}); 
	const data = useMemo(
		() => 
			rows.map((value,index)=>{return {...value,rowID:index};}),
		[rows]);

	const columns = cols;

	const filteredRows = useMemo(() => {
		if (!query && !filters) return data;
		let preFiltered=data.filter((obj)=>{
			for (const key of Object.keys(filters)) {

				if (!obj[key].toString().toLowerCase().includes(filters[key].toLowerCase())){
					return false;
				}
			}
			return true;});
		return preFiltered.filter((obj)=>Object.values(obj).toString().toLowerCase().includes(query));
	  }, [filters,query, data]);

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
			console.log(value);
			return columns[key].Cell(rowID,value);
		}else{
			return <Box>{value}</Box>;
		}
	};
	const renderHeader=(key)=>{
		return (<VStack>
			<Th>{columns[key].header}</Th>
			{(columns[key].hasOwnProperty('canFilter')&& columns[key].canFilter)&& (<Input type='text' onChange={
				(e)=>{setFilter((prev)=>({
					...prev,
					[key]:e.target.value
				}));}} />)
			}
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
		setSelected(preSelected);
		setSelectedRows(projects);
		setFilter({});
		setQuery('');
	}, [rows]);
	

	
	return (<>
		{rows.length>0 ?( <TableContainer maxW={'100%'} p={4}>
			<Input onChange={(e)=>{setQuery(e.target.value);}}/>
			<Table>
		  <Thead>
					<Tr key={'header'} >
						<Th ><Checkbox isChecked={data.length===selected.length}
							isIndeterminate={selected.length>0 && selected.length<data.length}
							onChange={(e)=>{onIntermediateCheckboxChange(e.target.checked);}}
									
						/></Th>
		  {Object.keys(columns).map(key => (
							<Th key={key} >
								{renderHeader(key)}	
							</Th>)
		  )}
		  </Tr>
		  </Thead>
		  <Tbody>
		  {filteredRows.map((row,index)=> (
						<Tr key={index}>
							<Td ><Checkbox defaultChecked={selected.includes(row.rowID)} isChecked={selected.includes(row.rowID)} onChange={(e) => handleCheck(row.rowID,e.target.checked)} /></Td>
							{Object.keys(columns).map((key)=>{

	 return <Td key={index+key} >{renderCell(key,row.rowID,row[key])}</Td>;
							})}</Tr>)
					)}
		 
		  </Tbody>
			</Table>
		</TableContainer>):(<Alert status='info'>
			<AlertIcon />
   No data to view
		</Alert>)}
	</>
	);
}

export default CustomTable;