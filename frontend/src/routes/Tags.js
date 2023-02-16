import { Grid, GridItem } from '@chakra-ui/react';

const Tags = () => {
	return (<Grid w='100%' templateColumns='repeat(5, 1fr)'>
		<GridItem colSpan={1}
			w='100%' h='10' bg='red.500' />
		<GridItem colSpan={4}
			w='100%' h='10' bg='gray.500' />
	</Grid>);
};
 
export default Tags;