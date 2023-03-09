import { Button, VStack } from '@chakra-ui/react';
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { fetchAssetSummary, filterAssets } from '../../api';
import AssetList from '../../components/AssetList';
import AssetSearcher from '../../components/AssetSearcher';
import AssetTable from '../../components/AssetTable';
const AssetsOverview = () => {
	const [assets, setAssets] = useState([]);
	let naviagte=useNavigate();

	const handleFilter = (searchData) => {
		filterAssets(searchData).then(res=>console.log(res.data));
	};


	useEffect(() => {
		fetchAssetSummary().then(res=>setAssets(res.data));
		console.log(assets);
	}, []);
	
	return (<VStack>
		<AssetTable assets={assets} setSelectedAssets={()=>{}} preSelIDs={[]} />
		<Button onClick={()=>naviagte('./new')}>Create Asset</Button>
		<AssetSearcher filerFunc={handleFilter}/>
	</VStack>);
};
 
export default AssetsOverview;