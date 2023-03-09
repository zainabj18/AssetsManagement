import {
	Button,
	HStack,
	VStack,
	Text,
	useBoolean,
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
		<VStack>
			<Text>Attribute Viewer</Text>
			<VStack>
				{attributes.map((attributes) => {
					return (
						<HStack key={attributes.attributeID}>
							<Text>{attributes.attributeName}</Text>
							{
								(user && user.userRole === 'ADMIN') &&
								<Button onClick={() => deleteThis(attributes)}>Delete</Button>
							}
						</HStack>

					);
				})}
			</VStack>
		</VStack>
	);
};

export default AttributeViewer;