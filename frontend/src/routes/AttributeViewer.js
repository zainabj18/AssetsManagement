import {
	Button, useBoolean,
	TableContainer, Table, TableCaption, Thead, Tbody, Th, Tr, Td
} from '@chakra-ui/react';
import { useEffect, useState } from 'react';
import useAuth from '../hooks/useAuth';
import { deleteAttribute, fetchAllAttributes, } from '../api';

const AttributeViewer = () => {
	const { user } = useAuth();
	const [toggle, set_toggle] = useBoolean();

	useEffect(() => {
		async function load_allAttributes() {
			let data = await fetchAllAttributes(res => res.data);
			console.log(data);
			set_attributes(data);
		}
		load_allAttributes();
	}, [toggle]);

	const [attributes, set_attributes] = useState([]);

	const deleteThis = (attribute) => {
		deleteAttribute(attribute.attributeID).then(data => {
			if (data.wasAllowed == false) {
				alert('Type ' + attribute.attributeName + ' is part of a type, can not be deleted.');
			}
			else {
				set_toggle.toggle();
			}
		});

	};

	return (
		<TableContainer>
			<Table>
				<TableCaption placement='top'>Attribute Viewer</TableCaption>
				<Thead>
					<Tr>
						<Th>Name</Th>
						<Th>Type</Th>
						<Th>Is Optional</Th>
						<Th>Delete</Th>
					</Tr>
				</Thead>
				<Tbody>
					{attributes.map((attributes) => {
						return (
							<Tr key={attributes.attributeID}>
								<Td>{attributes.attributeName}</Td>
								<Td>{attributes.attributeType}</Td>
								<Td>{attributes.validation.isOptional.toString()}</Td>
								<Td>
									{
										(user && user.userRole === 'ADMIN') &&
										<Button onClick={() => deleteThis(attributes)}>Delete</Button>
									}
								</Td>
							</Tr>

						);
					})}
				</Tbody>
			</Table>
		</TableContainer>
	);
};

export default AttributeViewer;