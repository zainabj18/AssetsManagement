import {
	Button,
	VStack,
	Table, Thead, Tbody, Tr, Th, Td, TableContainer, TableCaption,
	Text,
} from '@chakra-ui/react';
import { useEffect, useState } from 'react';
import { fetchAllTypes } from '../api';

const TypeViewer = () => {

	useEffect(() => {
		async function load_allTypes() {
			let data = await fetchAllTypes(res => res.data);
			set_types(data);
		}
		load_allTypes();
	}, []);

	const [types, set_types] = useState([]);

	return (
		<VStack>
			<Text>Type Viewer</Text>
			<TableContainer>
				<Table varient='simple'>
					<TableCaption placement='top' color='white'>Types</TableCaption>
					<Thead>
						<Tr>
							<Th color='white'>Type</Th>
							<Th color='white'>Attributes</Th>
							<Th color='white'>Attribute Data Type</Th>
						</Tr>
					</Thead>
					<Tbody>
						{types.map((types) => {
							return (
								<Tr key={types.typeName}>
									<Td>{types.typeName}</Td>
									<Td>
										{types.metadata.map((metadata) => {
											return (
												<VStack key={metadata.attributeName}>
													<Text>{metadata.attributeName}</Text>
												</VStack>
											);
										})}
									</Td>
									<Td>
										{types.metadata.map((metadata) => {
											return (
												<VStack key={metadata.attributeName}>
													<Text>{metadata.attributeType}</Text>
												</VStack>
											);
										})}
									</Td>
								</Tr>
							);
						})}
					</Tbody>
				</Table>
			</TableContainer>
			<Button>Create New</Button>
		</VStack>
	);
};

export default TypeViewer;