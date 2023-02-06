import { Heading, VStack } from '@chakra-ui/react';
import {Outlet} from 'react-router-dom';


const AssetsLayout= () => {
	return (<VStack>
		<Heading>Assets</Heading>
		<Outlet />
	</VStack>);
};
 
export default AssetsLayout;