import { Button, ButtonGroup, Heading,useBoolean,VStack } from '@chakra-ui/react';
import { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { copyToTag,deleteTag, fetchAssetsinTag, removeFromTag } from '../api';
import AssetTable from '../components/AssetTable';
import OperationTo from '../components/OperationTo';

const TagViewer = () => {
	const [assetsin, setAssets] = useState([]);
	const [selectedAssets, setSelectedAssets]=useState([]);
	const [tag, setTag] = useState('');
	const [trigger,setTrigger]=useBoolean();
	const { id } = useParams();
	let navigate = useNavigate();
	
	const getAssetIDs=()=>{
		return selectedAssets.map(
			(rowID)=>{return assetsin[rowID].asset_id;});
	};
	const handleRemove=()=>{
		let assetIDs=getAssetIDs();
		removeFromTag(id,assetIDs).then((res)=>{console.log(res); setTrigger.toggle();});
	};
	const handleCopy=(tag)=>{
		let assetIDs=getAssetIDs();
		copyToTag(tag,assetIDs).then((res)=>{console.log(res); setTrigger.toggle();});
	};
	const handleMove=(tag)=>{
		let assetIDs=getAssetIDs();
		copyToTag(tag,assetIDs).then((res)=>{removeFromTag(id,assetIDs);setTrigger.toggle();});
	};
	const handleDelete=()=>{
		deleteTag(id).then((res)=>{console.log(res);});
		navigate('/tags');
	};
	useEffect(() => {
		fetchAssetsinTag(id).then((res)=>{setAssets(res.data.assets);
			setTag(res.data.tag);});
	}, [id,trigger]);
    
	return ( <VStack bg={'whiteAlpha.500'} h={'100%'} w={'100%'} p={2}>
		<Heading>{tag}</Heading>
		<AssetTable assets={assetsin} setSelectedAssets={setSelectedAssets} preSelIDs={[]}/>
		<ButtonGroup>
			<Button onClick={handleRemove}>Remove from tag</Button>
			<OperationTo actionFunc={handleCopy} actionName="Copy" />
			<OperationTo actionFunc={handleMove} actionName="Move" />
			<Button colorScheme='red' onClick={handleDelete}>Delete</Button>
		</ButtonGroup>
	</VStack> );
};
 
export default TagViewer;