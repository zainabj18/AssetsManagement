import { Box, Flex, HStack, Input, useBoolean, VStack, } from '@chakra-ui/react';
import { useEffect, useState } from 'react';
import { Outlet } from 'react-router-dom';
import { fetchTags } from '../../api';
import CustomNavLink from '../../components/CustomNavLink';
import NewTag from '../../components/NewTag';

const Tags = () => {
	const [tags, setTags] = useState([]);
	const [results, setResults] = useState([]);
	const [trigger,setTrigger]=useBoolean();
	//trigger refresh of tags on create

	const filter=(value) => { 
		console.log(value);
		if (value===''){
			setResults(tags);
		}else{
			let filteredTag=tags.filter((t)=>t.name.toLowerCase().includes(value.toLowerCase()));
			setResults(filteredTag);
		}
	 };

	const [update, setUpdate] = useBoolean();

	useEffect(() => {
		fetchTags().then((res)=>{
			console.log('here');
			setTags(res.data);
			setResults(res.data);
		}
		);
	}, [trigger, update]);
	
	return (<Box w='75vw' minH='80vh' display={'flex'} flexDirection="row" p={2} border alignSelf={'center'}>
		<Box w='8wv' minH='100%' bg='gray.300' p={4} color='black' align={'top'}>
			<HStack>
				<Input type='text' placeholder='Search' onChange={(e)=>{filter(e.target.value);}}/>
				<NewTag trigger={setTrigger}/>
			</HStack>
			<VStack p={2}>
				{results.map((t,index)=>(
					<CustomNavLink key={index} to={`./${t.id}`} w='100%'>
						{t.name}
					</CustomNavLink>

				))}
				
			</VStack>
		</Box>
		<Box w='62vw' minH='100%' bg='white'>
			<Outlet context={[update, setUpdate]}/>
		</Box> 
	</Box>
	);
};
 
export default Tags;
