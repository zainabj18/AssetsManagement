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

function AssetList({assets}) {
	const data = React.useMemo(
		() => assets,
		[assets]
	);

	const columns = React.useMemo(
		() => [
			{
				Header: 'Asset ID',
				accessor: 'asset_id',
				Cell:row=><Link to={`view/${row.value}`} as={NavLink}>{row.value}</Link>
			},
			{
				Header: 'Asset Name',
				accessor: 'name',
			},
			{
				Header: 'Asset Type',
				accessor: 'type',
			},
			{
				Header: 'Asset Classification',
				accessor: 'classification',
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

export default ProjectList;