import { VStack } from '@chakra-ui/react';
import { useEffect, useState } from 'react';
import { fetchAssetSummary } from '../../api';
import AssetList from '../../components/AssetList';
import AssetSearcher from './../AssetSearcher';
const AssetsOverview = () => {
	const [assets, setAssets] = useState([]);
	useEffect(() => {
		fetchAssetSummary().then(res=>setAssets(res.data));
		console.log(assets);
	}, []);
	
	return (<VStack>
		<AssetList assets={assets}/>
		<AssetSearcher />
	</VStack>);
};
 
export default AssetsOverview;