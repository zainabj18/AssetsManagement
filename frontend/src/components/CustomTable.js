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
	AlertIcon,
	Text,
	IconButton,
	HStack
} from '@chakra-ui/react';
import {ArrowRightIcon,ArrowLeftIcon} from '@chakra-ui/icons';


function CustomTable({setSelectedRows,rows,cols,preSelIDs}) {
	const [selected,setSelected] = useState([]); 
	const [query,setQuery]= useState(''); 
	const [filters,setFilter]= useState({}); 
	const data = useMemo(
		() => 
			rows.map((value,index)=>{
				let filertedVals=(Object.fromEntries(Object.keys(cols).map(k => [k, value[k]])));
				return {...filertedVals,rowID:index};}),
		[rows]);

	const columns = cols;
	const pageSize = 15;
	const [currnetPage,setCurrnetPage]= useState(0); 

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
				setSelectedRows([...selected,rowID]);
				setSelected((prev)=>{return  [...prev,rowID];});	
			}
		}else {
			let newSelected=selected.filter((id) => id !==rowID);
			setSelected(newSelected);
			setSelectedRows(newSelected);
		}	
	};
	const renderCell=(key,rowID,value)=>{
		if (columns[key].hasOwnProperty('Cell')){
			return columns[key].Cell(data[rowID],value);
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
				}));}} placeholder={'Search '+columns[key].header} style={{textTransform:'capitalize',textOverflow: 'ellipsis'}}/>)
			}
		</VStack>);
		
	};

	const onIntermediateCheckboxChange=(val)=>{
		if (val){
			setSelected([...Array(data.length).keys()]);
			setSelectedRows([...Array(data.length).keys()]);
		}else{
			setSelected([]);
			setSelectedRows([]);
		}
	};

	const updatePage=(val)=>{
		setCurrnetPage(currnetPage + val);
	};

	useEffect(() => {
		console.log('new table');
		if (setSelectedRows){
			let preSelected=[];
			let row=[];
			for (let i = 0; i < data.length; i++) {
				let obj=data[i];
				if (obj.hasOwnProperty('isSelected')&obj.isSelected){
					preSelected.push(i);
					row.push(obj);
				}
			}
			for (let i = 0; i < preSelIDs.length; i++) {
				let obj=data[i];
				preSelected.push(i);
				row.push(obj);
			}
			setSelected(preSelected);
			setSelectedRows(row);
		}
		setCurrnetPage(0);
	}, [rows,cols]);
	

	
	return (<>
		{rows.length>0 ?( <TableContainer maxW={'100%'} p={4}>
			<Input onChange={(e)=>{setQuery(e.target.value);}} placeholder="Search table"/>
			<Table>
		  <Thead>
					<Tr key={'header'} >
						{setSelectedRows && <Th><Checkbox isChecked={data.length===selected.length}
							isIndeterminate={selected.length>0 && selected.length<data.length}
							onChange={(e)=>{onIntermediateCheckboxChange(e.target.checked);}}
									
						/></Th>}
		  {Object.keys(columns).map(key => (
							<Th key={key} >
								{renderHeader(key)}	
							</Th>)
		  )}
		  </Tr>
		  </Thead>
		  <Tbody>
		  {filteredRows.slice(currnetPage*pageSize,(currnetPage*pageSize)+pageSize).map((row,index)=> (
						<Tr key={index}>
							{setSelectedRows && <Td ><Checkbox defaultChecked={selected.includes(row.rowID)} isChecked={selected.includes(row.rowID)} onChange={(e) => handleCheck(row.rowID,e.target.checked)} /></Td>}
							{Object.keys(columns).map((key)=>{

	 return <Td key={index+key} >{renderCell(key,row.rowID,row[key])}</Td>;
							})}</Tr>)
					)}
		 
		  </Tbody>

					

			</Table>
			<HStack>
				<IconButton
					icon={<ArrowLeftIcon />}
					onClick={(e)=>updatePage(-1)}
					isDisabled={currnetPage===0}
				/>
				<Text>Page {currnetPage+1} of {Math.ceil(filteredRows.length/pageSize)}</Text>
				<IconButton
					icon={<ArrowRightIcon />}
					onClick={(e)=>updatePage(1)}
					isDisabled={currnetPage+1===Math.ceil(filteredRows.length/pageSize)}
				/>
				<Text>{filteredRows.length} row(s) found</Text>
			</HStack>
			
		</TableContainer>):(<Alert status='info'>
			<AlertIcon />
   No data to view
		</Alert>)}
	</>
	);
}

export default CustomTable;