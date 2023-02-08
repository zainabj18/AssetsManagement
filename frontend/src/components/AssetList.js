import React from 'react';
import { useTable, useRowSelect, useGlobalFilter } from 'react-table';

import {
	Table,
	Thead,
	Tbody,
	Tr,
	Th,
	Td,
	TableContainer
} from '@chakra-ui/react';
import IndeterminateCheckbox from './IndeterminateCheckbox';
import GlobalFilter from './GlobalFilter';


function AssetList() {
	const data = React.useMemo(
		() => [
			{
				id: 1,
				name: 'Programming Language',
				type: 'text',
				level: 'Public'
			},
			{
				id: 2,
				name: 'Number of Issues',
				type: 'Number',
				level: 'Restricted'
			},
			{
				id: 3,
				name: 'Authors',
				type: 'List',
				level: 'Confidential'
			},
		],
		[]
	);

	const columns = React.useMemo(
		() => [
			{
				Header: 'Asset ID',
				accessor: 'id',
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
				Header: 'Asset Access Level',
				accessor: 'level',
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
		useGlobalFilter,
		hooks => {
			hooks.visibleColumns.push(columns => [
				{
					id: 'selection',
					Header: ({ getToggleAllRowsSelectedProps }) => (
						<IndeterminateCheckbox {...getToggleAllRowsSelectedProps()} />
					),
					Cell: ({ row }) => (
						<IndeterminateCheckbox {...row.getToggleRowSelectedProps()} />
					),
				},
				...columns,
			]);
		}
	);


	return (<>

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
						d => d.original.id

					))}
				</code>
			</pre>
		</TableContainer>

	</>
	);
}

export default AssetList;