import { Button, VStack } from '@chakra-ui/react';
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { fetchAssetSummary, filterAssets } from '../../api';
import AssetList from '../../components/AssetList';
import AssetSearcher from '../../components/AssetSearcher';
import AssetTable from '../../components/AssetTable';
/**
 * return full name of the user
 * @param   {}
 *  a page for view assets 
 */
const AssetsOverview = () => {
	const [assets, setAssets] = useState([]);
	const [results, setResults] = useState([]);
	let naviagte=useNavigate();
/**
 * return full name of the user
 * @param   {string} searchData  filter assets
 */
	const handleFilter = (searchData) => {
		filterAssets(searchData).then(res=>{
			setResults(assets.filter((asset)=>res.data.includes(asset.asset_id)));
			console.log(res.data);});
	};


	useEffect(() => {
		fetchAssetSummary().then(res=>{
			setResults(res.data);
			setAssets(res.data);});
		console.log(assets);
	}, []);
	
	return (<VStack  width={"60vw"} background="white" paddingX={5} paddingY={5} rounded="2xl"  boxShadow="0 3px 6px #00000029">
		<AssetTable assets={results} setSelectedAssets={()=>{}} preSelIDs={[]} />
		<Button onClick={()=>naviagte('./new')} width="100%" paddingY={6}>Create Asset</Button>
		<AssetSearcher filerFunc={handleFilter}/>
	</VStack>);
};
 
export default AssetsOverview;