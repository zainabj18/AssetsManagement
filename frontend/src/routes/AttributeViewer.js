import {
	Button, useBoolean,
	TableContainer, Table, TableCaption, Thead, Tbody, Th, Tr, Td, VStack
} from '@chakra-ui/react';
import { useEffect, useState } from 'react';
import useAuth from '../hooks/useAuth';
import { deleteAttribute, fetchAllAttributes, } from '../api';
import AttributeModal from '../components/AttributeModal';

const AttributeViewer = () => {
	const { user } = useAuth();
	const [toggle, set_toggle] = useBoolean();

	useEffect(() => {
		async function load_allAttributes() {
			let data = await fetchAllAttributes(res => res.data);
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
		<VStack height={"85vh"}>
		<div style={{height:"72vh",overflow:'scroll'}}>
				<Table>
					{/* <TableCaption placement='top'>Attribute Viewer</TableCaption> */}
					<Thead zIndex={999}>
						<Tr>
							<Th>Name</Th>
							<Th>Type</Th>
							<Th>Is Optional</Th>
							<Th>Delete</Th>
						</Tr>
					</Thead>
					<Tbody zIndex={-99}>
						{attributes.map((attributes) => {
							return (
								<Tr key={attributes.attributeID} zIndex={-1}>
									<Td>{attributes.attributeName}</Td>
									<Td>{attributes.attributeType}</Td>
									<Td>{attributes.validation.isOptional.toString()}</Td>
									<Td>
										{
											(user && user.userRole === 'ADMIN') &&
											<div style={{background:'#ed7966',padding:5,borderRadius:5,color:"#fff"}}   onClick={() => deleteThis(attributes)}>Delete</div >
										}
									</Td>
								</Tr>

							);
						})}
					</Tbody>
				</Table>
				</div>
			<AttributeModal showModalButtonText='New' load_allAttributes_setter={set_toggle}/>
		</VStack>
	);
};

export default AttributeViewer;