import React, { useEffect, useMemo, useState } from 'react';
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
	border,
	Text,
	IconButton,
	HStack
} from '@chakra-ui/react';
import { ArrowRightIcon, ArrowLeftIcon } from '@chakra-ui/icons';


function CustomTable({ setSelectedRows, rows, cols, preSelIDs }) {
	const [selected, setSelected] = useState([]);
	const [query, setQuery] = useState('');
	const [filters, setFilter] = useState({});
	const data = useMemo(
		() => 
			rows.map((value,index)=>{
				let filertedVals=(Object.fromEntries(Object.keys(cols).map(k => [k, value[k]])));
				let isSelected=value.hasOwnProperty('isSelected')&value.isSelected;
				return {...filertedVals,rowID:index,rows,isSelected:isSelected};}),
		[rows]);

	const columns = cols;
	const pageSize = 15;
	const [currnetPage, setCurrnetPage] = useState(0);

	const filteredRows = useMemo(() => {
		if (!query && !filters) return data;
		let preFiltered = data.filter((obj) => {
			for (const key of Object.keys(filters)) {

				if (!obj[key].toString().toLowerCase().includes(filters[key].toLowerCase())) {
					return false;
				}
			}
			return true;
		});
		return preFiltered.filter((obj) => Object.values(obj).toString().toLowerCase().includes(query));
	}, [filters, query, data]);

	const handleCheck = (rowID, val) => {
		if (val) {
			if (!selected.includes(rowID)) {
				setSelectedRows([...selected, rowID]);
				setSelected((prev) => { return [...prev, rowID]; });
			}
		} else {
			let newSelected = selected.filter((id) => id !== rowID);
			setSelected(newSelected);
			setSelectedRows(newSelected);
		}
	};
	const renderCell = (key, rowID, value) => {
		if (columns[key].hasOwnProperty('Cell')) {
			return columns[key].Cell(data[rowID], value);
		} else {
			return <Box>{value}</Box>;
		}
	};
	const renderHeader = (key) => {
		return (<VStack>
			<Th color='white'>{columns[key].header}</Th>
			{(columns[key].hasOwnProperty('canFilter') && columns[key].canFilter) && (<Input type='text' onChange={
				(e) => {
					setFilter((prev) => ({
						...prev,
						[key]: e.target.value
					}));
				}} placeholder={'Search ' + columns[key].header} bg='white' border='1px solid' style={{ textTransform: 'capitalize', textOverflow: 'ellipsis' }} />)
			}
		</VStack>);

	};

	const onIntermediateCheckboxChange = (val) => {
		if (val) {
			setSelected([...Array(data.length).keys()]);
			setSelectedRows([...Array(data.length).keys()]);
		} else {
			setSelected([]);
			setSelectedRows([]);
		}
	};

	const updatePage = (val) => {
		setCurrnetPage(currnetPage + val);
	};

	useEffect(() => {
		console.log('new table hello');
		console.log(data);
		if (setSelectedRows){
			let preSelected=[];
		
			for (let i = 0; i < preSelIDs.length; i++) {
				preSelected.push(i);
			}
			console.log('hello in custome table ');
			console.log(preSelIDs);
			setSelected(preSelIDs);
		}
		
	
		setCurrnetPage(0);
	}, [rows, cols]);



	return (<>
		{rows.length > 0 ? (<TableContainer maxW={'100%'} p={4}>
			<Input onChange={(e) => { setQuery(e.target.value); }} placeholder='Search' bg='white' border='1px solid' />
			<Table>
				<Thead border={'1px solid'} position='sticky' top={0}>
					<Tr key={'header'} >
						{setSelectedRows && <Th bg='#0a2861'>
							<Checkbox isChecked={data.length === selected.length}
								isIndeterminate={selected.length > 0 && selected.length < data.length}
								onChange={(e) => { onIntermediateCheckboxChange(e.target.checked); }}
								border='1px solid white'
								marginTop={3}

							/></Th>}
						{Object.keys(columns).map(key => (
							<Th key={key} bg='#0a2861' >
								{renderHeader(key)}
							</Th>)
						)}
					</Tr>
				</Thead>
				<Tbody>
					{filteredRows.slice(currnetPage * pageSize, (currnetPage * pageSize) + pageSize).map((row, index) => (
						<Tr key={index} bg='white'>
							{setSelectedRows && <Td bg='white'><Checkbox defaultChecked={selected.includes(row.rowID)} isChecked={selected.includes(row.rowID)} onChange={(e) => handleCheck(row.rowID, e.target.checked)} /></Td>}
							{Object.keys(columns).map((key) => {

								return <Td key={index + key} bg='white' >{renderCell(key, row.rowID, row[key])}</Td>;
							})}</Tr>)
					)}
				</Tbody>
			</Table>
			<HStack>
				<IconButton
					icon={<ArrowLeftIcon />}
					onClick={(e) => updatePage(-1)}
					isDisabled={currnetPage === 0}
				/>
				<Text>Page {currnetPage + 1} of {Math.ceil(filteredRows.length / pageSize)}</Text>
				<IconButton
					icon={<ArrowRightIcon />}
					onClick={(e) => updatePage(1)}
					isDisabled={currnetPage + 1 === Math.ceil(filteredRows.length / pageSize)}
				/>
				<Text>{filteredRows.length} row(s) found</Text>
			</HStack>
		</TableContainer>) : (<Alert status='info' background={'rgb(74 74 74 / 19%)'} paddingY={5} borderRadius={10} margin={5} >
			<AlertIcon />
			No data to view
		</Alert>)}
	</>
	);
}

export default CustomTable;