import { Box, HStack} from '@chakra-ui/react';
import { Outlet } from 'react-router-dom';
import CustomNavLink from './CustomNavLink';

const AssetOverview=() => {
	return ( 
		<Box>
			<HStack>
				<CustomNavLink to={'./'}>Attributes</CustomNavLink>
			</HStack>
			<Box>
				<Outlet />
			</Box>
		</Box>);
};
 
export default AssetOverview
;