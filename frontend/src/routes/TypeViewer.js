import {
	Button,
	VStack,
	Table, Thead, Tbody, Tr, Th, Td, TableContainer, TableCaption,
	Text,
	useBoolean,
} from '@chakra-ui/react';
import { useEffect, useState } from 'react';
import { Link as RouteLink } from 'react-router-dom';
import { deleteType, fetchAllTypes } from '../api';
import useAuth from '../hooks/useAuth';

const TypeViewer = () => {
	const { user } = useAuth();
	const [toggle, set_toggle] = useBoolean();

	useEffect(() => {
		async function load_allTypes() {
			let data = await fetchAllTypes(res => res.data);
			set_types(data);
		}
		load_allTypes();
	}, [toggle]);

	const [types, set_types] = useState([]);

	const deleteThis = (type) => {
		deleteType(type.typeId).then(data => {
			if (data.wasAllowed == false) {
				alert('Type ' + type.typeName + ' is depended upon, can not be deleted.');
			}
			else {
				set_toggle.toggle();
			}
		});

	};

	return (
		<VStack>
			<TableContainer>
				<Table varient='simple'>
					<TableCaption placement='top' color='white'>Types</TableCaption>
					<Thead>
						<Tr>
							<Th color='white'>Type</Th>
							<Th color='white'>Attributes</Th>
							<Th color='white'>Attribute Data Type</Th>
							<Th color='white'>Delete</Th>
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
									<Td>
										<Button onClick={() => deleteThis(types)}>Delete</Button>
									</Td>
								</Tr>
							);
						})}
					</Tbody>
				</Table>
			</TableContainer>
			{(user && user.userRole === 'ADMIN') && <RouteLink to='adder'>
				<Button>New</Button>
			</RouteLink>}
		</VStack>
	);
};

export default TypeViewer;