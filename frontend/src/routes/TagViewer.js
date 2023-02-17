import { Heading, List,ListItem, VStack } from '@chakra-ui/react';
import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { fetchAssetsinTag } from '../api';
import CustomTable from '../components/CustomTable';

const TagViewer = () => {
	const [assets, setAssets] = useState([]);
	const [tag, setTag] = useState('');
	const { id } = useParams();

	useEffect(() => {
		fetchAssetsinTag(id).then((res)=>{setAssets(res.data.assets);
			setTag(res.data.tag);});
		console.log(assets);
	}, [id]);
    
	return ( <VStack bg={'whiteAlpha.200'} h={'100%'} w={'100%'} >
		<Heading>{tag}</Heading>
		<CustomTable rows={assets} setSelectedRows={()=>{}}/>
	</VStack> );
};
 
export default TagViewer;