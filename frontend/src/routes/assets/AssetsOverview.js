import { Button, VStack } from '@chakra-ui/react';
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { fetchAssetSummary } from '../../api';
import AssetList from '../../components/AssetList';
import AssetSearcher from '../../components/AssetSearcher';
const AssetsOverview = () => {
	const [assets, setAssets] = useState([]);
	let naviagte=useNavigate();
	useEffect(() => {
		fetchAssetSummary().then(res=>setAssets(res.data));
		console.log(assets);
	}, []);
	
	return (<VStack>
		<AssetList assets={assets}/>
		<Button onClick={()=>naviagte('./new')}>Create Asset</Button>
		<AssetSearcher />
	</VStack>);
};
 
export default AssetsOverview;