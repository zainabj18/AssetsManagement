import React from 'react';
import { useTable,useRowSelect } from 'react-table';

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
 

function ProjectSelect() {
	const data = React.useMemo(
		() => [
			{
				id:1,
				name: 'General',
				desc: 'Basic project',
			},
			{
				id:2,
				name: 'LAPD',
				desc: 'Basic project'
			},
			{
				id:3,
				name: 'Test',
				desc: 'Test project'
			},
		],
		[]
	);
 
	const columns = React.useMemo(
		() => [
			{
				Header: 'Project ID',
				accessor: 'id',
			},
			{
				Header: 'Project Name',
				accessor: 'name',
			},
			{
				Header: 'Project Decription',
				accessor: 'desc',
			}
		],
		[]
	);

	const {
		getTableProps,
		getTableBodyProps,
		headerGroups,
		rows,
		prepareRow,
		selectedFlatRows,
		state: { selectedRowIds },
	} = useTable(
		{
			columns,
			data,
		},
		useRowSelect,
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

					))}
				</code>
			</pre>
		</TableContainer>
	);
}

export default ProjectSelect;