import { Badge, Button, ButtonGroup, Heading,Modal,ModalBody,ModalCloseButton,ModalContent,ModalFooter,ModalHeader,ModalOverlay,useBoolean,useDisclosure,VStack } from '@chakra-ui/react';
import { useEffect, useMemo, useState } from 'react';
import { useParams } from 'react-router-dom';
import { copyAssetsinTag, copyRemoveFromTag, copyToTag, createTag, fetchAssetsinTag, fetchTags, removeFromTag } from '../api';
import AssetTable from '../components/AssetTable';
import CopyTo from '../components/CopyTo';
import SearchSelect from '../components/SearchSelect';

const TagViewer = () => {
	const [assetsin, setAssets] = useState([]);
	const [selectedAssets, setSelectedAssets]=useState([]);
	const [tag, setTag] = useState('');
	const [trigger,setTrigger]=useBoolean();
	const { id } = useParams();
	

	const handleRemove=()=>{
		let assetIDs=selectedAssets.map(
			(rowID)=>{return assetsin[rowID].asset_id;});
		removeFromTag(id,assetIDs).then((res)=>{console.log(res); setTrigger.toggle();});
	};
	const handleCopy=(tag)=>{
		let assetIDs=selectedAssets.map(
			(rowID)=>{return assetsin[rowID].asset_id;});
		copyToTag(tag,assetIDs).then((res)=>{console.log(res); setTrigger.toggle();});
	};
	useEffect(() => {
		fetchAssetsinTag(id).then((res)=>{setAssets(res.data.assets);
			setTag(res.data.tag);});
	}, [id,trigger]);
    
	return ( <VStack bg={'whiteAlpha.500'} h={'100%'} w={'100%'} p={2}>
		<Heading>{tag}</Heading>
		<AssetTable assets={assetsin} setSelectedAssets={setSelectedAssets}/>
		<ButtonGroup>
			<Button onClick={handleRemove}>Remove from tag</Button>
			<CopyTo copyFunc={handleCopy} />
			
		</ButtonGroup>
	</VStack> );
};
 
export default TagViewer;