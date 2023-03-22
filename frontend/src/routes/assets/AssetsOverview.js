import { Button, VStack } from '@chakra-ui/react';
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { fetchAssetSummary, filterAssets } from '../../api';
import AssetSearcher from '../../components/assets/AssetSearcher';
import AssetTable from '../../components/assets/AssetTable';
const AssetsOverview = () => {
	const [assets, setAssets] = useState([]);
	const [results, setResults] = useState([]);
	let naviagte=useNavigate();

	const handleFilter = (searchData) => {
		filterAssets(searchData).then(res=>{
			setResults(assets.filter((asset)=>res.data.includes(asset.assetID)));
			console.log(assets.filter((asset)=>res.data.includes(asset.assetID)));
			console.log(res.data);});
	};


	useEffect(() => {
		fetchAssetSummary().then(res=>{
			setResults(res.data);
			setAssets(res.data);});
		console.log(assets);
	}, []);
	
	return (<VStack>
		<AssetTable assets={results} setSelectedAssets={null} preSelIDs={[]} />
		<Button onClick={()=>naviagte('./new')}>Create Asset</Button>
		<AssetSearcher filerFunc={handleFilter}/>
	</VStack>);
};
 
export default AssetsOverview;