import {Heading, VStack } from '@chakra-ui/react';
import { useEffect, useState } from 'react';
import { fetchMyAssetSummary} from '../../api';
import AssetTable from '../../components/assets/AssetTable';
const MyAssets = () => {
	const [assets, setAssets] = useState([]);
	useEffect(() => {
		fetchMyAssetSummary().then(res=>{
			setAssets(res.data);});
	}, []);
	
	return (<VStack>
		<Heading>My Assets</Heading>
		<AssetTable assets={assets} setSelectedAssets={null} preSelIDs={[]} />
	</VStack>);
};
 
export default MyAssets;