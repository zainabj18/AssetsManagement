import {
	Button,
	VStack,
	Table, Thead, Tbody, Tr, Th, Td, TableContainer, TableCaption,
	Text,
} from '@chakra-ui/react';
import { useState } from 'react';

const TypeViewer = () => {

	const [types, setTypes] = useState([
		/** Dummy Data */
		{
			typeName: 'framework',
			metadata: [
				{
					attributeName: 'programming Language(s)',
					attributeType: 'text',
				},
				{
					attributeName: 'public',
					attributeType: 'checkbox',
				},
				{
					attributeName: 'no. of issues',
					attributeType: 'number',
				},
				{
					attributeName: 'built on',
					attributeType: 'datetime-local',
				},
				{
					attributeName: 'version',
					attributeType: 'text',
				},
				{
					attributeName: 'stars',
					attributeType: 'num_lmt',
					validation: {
						min: 1,
						max: 5
					}
				},
				{
					attributeName: 'license',
					attributeType: 'options',
					validation: {
						values: ['MIT', 'GNU'],
						isMulti: true
					}
				},
				{
					attributeName: 'authors',
					attributeType: 'list',
					validation: {
						type: 'text'
					}
				},
				{
					attributeName: 'authors_emails',
					attributeType: 'list',
					validation: {
						type: 'email'
					}
				},
				{
					attributeName: 'authors_emails_domain',
					attributeType: 'list',
					validation: {
						type: 'url'
					}
				}
			]
		},
		{
			typeName: 'library',
			metadata: [
				{
					attributeName: 'platform',
					attributeType: 'text',
				},
				{
					attributeName: 'private',
					attributeType: 'checkbox',
				},
				{
					attributeName: 'last modified',
					attributeType: 'datetime-local',
				},
				{
					attributeName: 'description',
					attributeType: 'text',
				},
				{
					attributeName: 'fileSize(kb)',
					attributeType: 'number',
				}
			]
		}
		/** End of Dummy Data */
	]);

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
							<Th color='white'>View</Th>
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
										<Button>View</Button>
									</Td>
								</Tr>
							);
						})}
					</Tbody>
				</Table>
			</TableContainer>
		</VStack>
	);
};

export default TypeViewer;