import { Box, Flex, HStack, Input, VStack, } from '@chakra-ui/react';
import { useEffect, useState } from 'react';
import { Outlet } from 'react-router-dom';
import { fetchTags } from '../api';
import CustomNavLink from '../components/CustomNavLink';
import NewTag from '../components/NewTag';

const Tags = () => {
	const [tags, setTags] = useState([]);
	//trigger refresh of tags on create

	useEffect(() => {
		fetchTags().then((res)=>{
			setTags(res.data);
		}
		);
	
	}, []);
	
	return (<Flex w='100%' minH='80vh' alignItems={'stretch'} p={2} border>
		<Box w='30%' minH='100%' bg='gray.300' p={4} color='black' align={'top'}>
			<HStack>
				<Input type='text' placeholder='Search for tag ...'/>
				<NewTag />
			</HStack>
			<VStack p={2}>
				{tags.map((t,index)=>(
					<CustomNavLink key={index} to={`./${t.id}`} w='100%'>
						{t.name}
					</CustomNavLink>

				))}
				
			</VStack>
		</Box>
		<Box w='70%' minH='100%' bg='white'>
			<Outlet />
		</Box> 
	</Flex>
	);
};
 
export default Tags;
