import {
	Table, Thead, Tbody, Tr, Th, Td, TableContainer,
	Heading,
} from '@chakra-ui/react';

const SelectedAttributesList = ({selectedAttributes_state}) => {
	return (
		<TableContainer>
			<Heading placement='top' size="md">Selected Attributes</Heading>
			<Table varient='simple'>

				<Thead>
					<Tr>
						<Th color='white'>Attribute Name</Th>
						<Th color='white'>Data Type</Th>
					</Tr>
				</Thead>
				<Tbody>
					{selectedAttributes_state.map((attribute) => {
						return (
							<Tr key={attribute.attributeName}>
								<Td>{attribute.attributeName}</Td>
								<Td>{attribute.attributeType}</Td>
							</Tr>
						);
					})}
				</Tbody>
			</Table>
		</TableContainer>
	);
};

export default SelectedAttributesList;