import React from 'react';
import { useTable,useRowSelect } from 'react-table';

import {
	Table,
	Thead,
	Tbody,
	Tr,
	Th,
	Td,
	TableContainer,
	Checkbox,
} from '@chakra-ui/react';
 
function ProjectSelect() {
	const data = React.useMemo(
		() => [
			{
				col1: 'General',
			},
			{
				col1: 'LAPD',
			},
			{
				col1: 'Project A',
			},
		],
		[]
	);
 
	const columns = React.useMemo(
		() => [
			{
				Header: 'Project Name',
				accessor: 'col1',
			}
		],
		[]
	);
 
	const {
		getTableProps,
		getTableBodyProps,
		headerGroups,
		rows,
		prepareRow
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
					Header: () => (
						<Checkbox />
					),
					Cell: () => (
						<Checkbox />
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
		</TableContainer>
	);
}

export default ProjectSelect;