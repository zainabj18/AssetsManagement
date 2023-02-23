import { Button, ButtonGroup, Editable, EditableInput, EditablePreview, Heading,IconButton,Input,Tooltip,useBoolean,useEditableControls,VStack } from '@chakra-ui/react';
import { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { copyToTag,deleteTag, fetchAssetsinTag, removeFromTag, updateTag } from '../api';
import AssetTable from '../components/AssetTable';
import OperationTo from '../components/OperationTo';
import useAuth from '../hooks/useAuth';

const SaveControl = () => {
	const {
		isEditing,
		getSubmitButtonProps
	  } = useEditableControls();
	  return isEditing && <Button {...getSubmitButtonProps()} >Save</Button>;
	
};
const TagViewer = () => {
	const { user } = useAuth();
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
		setTrigger.toggle();
		navigate(0);
		navigate('/tags');
	};

	const handleRename=(t)=>{
		updateTag(id,{id:id,name:t});
	};
	useEffect(() => {
		fetchAssetsinTag(id).then((res)=>{setAssets(res.data.assets);
			setTag(res.data.tag);});
		;
	}, [id,trigger,user]);
    
	return ( <VStack bg={'whiteAlpha.500'} h={'100%'} w={'100%'} p={2}>
		{tag &&<Editable
			textAlign="center"
			defaultValue={tag}
			startWithEditView={false}
			submitOnBlur={false}
			isDisabled={!(user && user.userRole === 'ADMIN')}
			alignItems='left' 
			alignContent='left'
			onSubmit={(e) => {
				handleRename(e);
			}}
			width="full"
			fontSize='6xl'
		>
			<Tooltip label={(user && user.userRole === 'ADMIN') ? 'Click to edit name':''}>
				<EditablePreview px={6} minW={'100%'}  bgSize={'400px'} />
			</Tooltip>
			<Input type='text' as={EditableInput}/>	
			<SaveControl />
		</Editable>}
		<AssetTable assets={assetsin} setSelectedAssets={setSelectedAssets} preSelIDs={[]}/>
		<ButtonGroup>
			<Button onClick={handleRemove}>Remove from tag</Button>
			<OperationTo actionFunc={handleCopy} actionName="Copy" />
			<OperationTo actionFunc={handleMove} actionName="Move" />
			<Button colorScheme='red' variant={'solid'} onClick={handleDelete}>Delete Tag</Button>
		</ButtonGroup>
	</VStack> );
};
 
export default TagViewer;