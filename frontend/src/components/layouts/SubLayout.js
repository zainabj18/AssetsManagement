import {Heading, VStack } from '@chakra-ui/react';
import {Outlet} from 'react-router-dom';


const SubLayout= ({name}) => {
	return (<VStack minH={'100vh'}>
		{/* <Heading>{name}</Heading> */}
		<Outlet  />
	</VStack>);
};
 
export default SubLayout;