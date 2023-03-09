import React from 'react';
import { useTable, useRowSelect, useGlobalFilter } from 'react-table';

import {
	Table,
	Thead,
	Tbody,
	Tr,
	Th,
	Td,
	TableContainer,
	Link
} from '@chakra-ui/react';
import { Link as NavLink } from 'react-router-dom';
import GlobalFilter from './GlobalFilter';

const AssetTable = ({assets,setSelectedAssets,preSelIDs,cols}) => {
	const [colours,setColors]=useState({});
	const columns =useMemo(()=>
	{ 
		console.log(cols);
		let orginal={
			'asset_id':{
				header: 'Asset ID',
				canFilter:true,
				Cell:(rowID,value)=><Link to={`/assets/view/${value}`} as={NavLink}>{value}</Link>
			},
			'name':{
				header: 'Asset Name',
				canFilter:true
			},
			'type':{
				header: 'Asset Type',
				canFilter:true
			},
			'classification':{
				header: 'Asset Classification',
				canFilter:true,
				Cell:(rowID,value)=>{return <Badge bg={colours[value]} color={'white'}>{value}</Badge>;}
			},
		};
		if (cols){
			orginal={...orginal,...cols};
		}
		return orginal;
	}
    ,[colours]);


function ProjectList({projects}) {
	const data = React.useMemo(
		() => projects,
		[projects]
	);

	const columns = React.useMemo(
		() => [
			{
				Header: 'Project ID',
				accessor: 'project_id',
				Cell:row=><Link to={`view/${row.value}`} as={NavLink}>{row.value}</Link>
			},
			{
				Header: 'Project Name',
				accessor: 'name',
			},
			{
				Header: 'Project Type',
				accessor: 'type',
			},
			{
				Header: 'Project members',
				accessor: 'members',
			}
		],
		[]
	);

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
		useGlobalFilter
	);


	return (<>

		<TableContainer>
			<GlobalFilter
				globalFilter={state.globalFilter}
				setGlobalFilter={setGlobalFilter}
			/>
			<Table {...getTableProps()} color={'white'}>
				<Thead >
					{headerGroups.map(headerGroup => (
						<Tr {...headerGroup.getHeaderGroupProps()}>
							{headerGroup.headers.map(column => (
								<Th
									{...column.getHeaderProps()}
									color={'white'}
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
						d => d.original.id

					))}
				</code>
			</pre>
		</TableContainer>

	</>
	);
}
}
