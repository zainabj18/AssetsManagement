import { Box, Container, HStack } from '@chakra-ui/react';
import { Outlet } from 'react-router-dom';
import CustomNavLink from './CustomNavLink';

const AssetOverview = () => {
	return (
		<Container minW='100%'>
			<HStack spacing={2} p={4}>
				<CustomNavLink to={'./'}>Attributes</CustomNavLink>
				<CustomNavLink to={'./classification'}>Classification</CustomNavLink>
				<CustomNavLink to={'./type'}>Type</CustomNavLink>
				<CustomNavLink to={'./tags'}>Tags</CustomNavLink>
				<CustomNavLink to={'./projects'}>Projects</CustomNavLink>
				<CustomNavLink to={'./outgoing'}>Outgoing Asset Links</CustomNavLink>
				<CustomNavLink to={'./incomming'}>Incomming Asset Links</CustomNavLink>
				<CustomNavLink to={'./graph'}>Related Assets Graph View</CustomNavLink>
			</HStack>
			<Box minW='100%'>
				<Outlet />
			</Box>
		</Container>);
};

export default AssetOverview
	;
