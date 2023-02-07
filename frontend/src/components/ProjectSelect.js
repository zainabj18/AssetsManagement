import React from 'react';
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
	HStack
} from '@chakra-ui/react';
import IndeterminateCheckbox from './IndeterminateCheckbox';
import GlobalFilter from './GlobalFilter';

function ProjectSelect({setSelectedProjects,projects}) {
	const { isOpen, onOpen, onClose } = useDisclosure();
	const data = React.useMemo(
		() => 
			[...projects],
		[projects]);
 
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
				accessor: 'description',
			}
		],
		[]
	);

	const addProjects=()=>{
		let selectedProjects=selectedFlatRows.map(
			(d)=>{
				return {'id':d.original.id,'name':d.original.name};}
		);
		console.log(addProjects);
		setSelectedProjects(selectedProjects);
		onClose();
	};

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
			initialState:{selectedRowIds: {0:true}}
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
		},
		
	);
    
 
	return (<>
		<Button onClick={onOpen}>Select Projects</Button>
		<Modal isOpen={isOpen} onClose={onClose} size={'full'}>
			<ModalOverlay />
			<ModalContent>
				<ModalHeader>Project Select</ModalHeader>
				<ModalCloseButton />
				<ModalBody>
					{projects && <TableContainer>
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

								))}
							</code>
						</pre>
					</TableContainer>}
				</ModalBody>

				<ModalFooter>
					<HStack>
						<Button onClick={addProjects}>Save</Button>
					</HStack>	
				</ModalFooter>
			</ModalContent>
			
		</Modal>
	</>
	);
}

export default ProjectSelect;