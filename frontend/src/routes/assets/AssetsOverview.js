import { Button, Heading, HStack, VStack } from '@chakra-ui/react';
import { useEffect, useState } from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { fetchAssetSummary, filterAssets } from '../../api';
import AssetSearcher from '../../components/assets/AssetSearcher';
import AssetTable from '../../components/assets/AssetTable';
const AssetsOverview = () => {
	const [assets, setAssets] = useState([]);
	const [results, setResults] = useState([]);
	let naviagte = useNavigate();
	/**
	 * return full name of the user
	 * @param   {string} searchData  filter assets
	 */
	const handleFilter = (searchData) => {
		filterAssets(searchData).then(res => {
			setResults(assets.filter((asset) => res.data.includes(asset.assetID)));
			console.log(assets.filter((asset) => res.data.includes(asset.assetID)));
			console.log(res.data);
		});
	};


	useEffect(() => {
		fetchAssetSummary().then(res => {
			setResults(res.data);
			setAssets(res.data);
		});
		console.log(assets);
	}, []);

	return (<VStack width={'100vw'} height={'80vh'} background='white' justifyContent={'space-between'} overflow='auto' flexDirection={'row-reverse'} display='flex' paddingX={5} paddingY={5} rounded='2xl' boxShadow='0 3px 6px #00000029'>
		<div style={{ width: '75vw', flexDirection: 'column', justifyContent: 'center', display: 'flex' }} >
			<div style={{ width: '75vw', overflow: 'hidden' }}>
				<AssetTable assets={results} setSelectedAssets={null} preSelIDs={[]} />
				
			</div>
			<VStack>
				<NavLink to="./graph"><Heading>View Graph</Heading></NavLink>
				<Button onClick={() => naviagte('./new')} width='50%' paddingY={6} alignSelf='center'>Create Asset</Button>
			</VStack>
			
		</div>
		<div style={{ width: '20vw', overflow: 'auto', height: '70vh' }}>
			<AssetSearcher filerFunc={handleFilter} />
		</div>
	</VStack>);
};

export default AssetsOverview;