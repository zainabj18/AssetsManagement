import { Badge, Heading,VStack } from '@chakra-ui/react';
import { useEffect, useMemo, useState } from 'react';
import { useParams } from 'react-router-dom';
import { fetchAssetsinTag } from '../api';
import AssetTable from '../components/AssetTable';
import CustomTable from '../components/CustomTable';

const TagViewer = () => {
	const [assetsin, setAssets] = useState([]);
	const [tag, setTag] = useState('');
	const { id } = useParams();

	useEffect(() => {
		fetchAssetsinTag(id).then((res)=>{setAssets(res.data.assets);
			setTag(res.data.tag);});
		console.log(assetsin);
	}, [id]);
    
	return ( <VStack bg={'whiteAlpha.500'} h={'100%'} w={'100%'} p={2}>
		<Heading>{tag}</Heading>
		<AssetTable assets={assetsin} setSelectedRows={()=>{}}/>
	</VStack> );
};
 
export default TagViewer;