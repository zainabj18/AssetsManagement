import { Stat, StatGroup,StatLabel, StatNumber } from '@chakra-ui/react';

const AssetsStats = ({created_at,last_modified_at}) => {
	return (<StatGroup>
		<Stat>
			<StatLabel>Created At</StatLabel>
			<StatNumber>{new Date(created_at).toLocaleString()}</StatNumber>
		</Stat>
		<Stat>
			<StatLabel>Last Modified</StatLabel>
			<StatNumber>{new Date(last_modified_at).toLocaleString()}</StatNumber>
		</Stat>
	</StatGroup>);
};
 
export default AssetsStats;