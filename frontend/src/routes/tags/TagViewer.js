import { Button, ButtonGroup, Editable, EditableInput, EditablePreview, Input, Tooltip, useBoolean, useEditableControls, useToast, VStack } from '@chakra-ui/react';
import { useEffect, useState } from 'react';
import { useNavigate, useParams, useOutletContext } from 'react-router-dom';
import { copyToTag, deleteTag, fetchAssetsinTag, removeFromTag, updateTag } from '../../api';
import AssetTable from '../../components/assets/AssetTable';
import OperationTo from '../../components/OperationTo';
import useAuth from '../../hooks/useAuth';

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
	const [selectedAssets, setSelectedAssets] = useState([]);
	const [tag, setTag] = useState('');
	const [trigger, setTrigger] = useBoolean();
	const { id } = useParams();
	const [update, setUpdate] = useOutletContext();
	const toast = useToast();

	let navigate = useNavigate();

	const getAssetIDs = () => {
		return selectedAssets.map(
			(rowID) => { return assetsin[rowID].assetID; });
	};
	const handleRemove = () => {
		let assetIDs = getAssetIDs();
		removeFromTag(id, assetIDs).then((res) => { console.log(res); setTrigger.toggle(); setUpdate.toggle(); }).catch(err=>toast({
			title: 'An error has occured'
		  }));;
	};
	const handleCopy = (tag) => {
		let assetIDs = getAssetIDs();
		copyToTag(tag, assetIDs).then((res) => { console.log(res); setTrigger.toggle(); setUpdate.toggle(); }).catch(err=>toast({
			title: 'An error has occured'
		  }));;
	};
	const handleMove = (tag) => {
		let assetIDs = getAssetIDs();
		copyToTag(tag, assetIDs).then((res) => { removeFromTag(id, assetIDs); setTrigger.toggle(); setUpdate.toggle(); }).catch(err=>toast({
			title: 'An error has occured'
		  }));;
	};
	const handleDelete = () => {
		deleteTag(id).then((res) => {navigate(0);}).catch(err=>toast({
			title: 'An error has occured'
		  }));;
		setTrigger.toggle();
		setUpdate.toggle();
		navigate('/tags');
	};

	const handleRename = (t) => {
		updateTag(id, { id: id, name: t }).then(
			res=>navigate(0)
		).catch(err=>toast({
			title: 'An error has occured'
		  }));
	};
	useEffect(() => {
		fetchAssetsinTag(id).then((res) => {
			console.log(res.data.tag);
			setAssets(res.data.assets);
			setTag(res.data.tag.name);

		});
		;
	}, [id, trigger, user]);

	return (<VStack bg={'whiteAlpha.500'} h={'100vh'} w={'100vw'} >
		{tag && <Editable
			textAlign="center"
			submitOnBlur={false}
			isDisabled={!(user && user.userRole === 'ADMIN')}
			alignItems='left'
			alignContent='left'
			onSubmit={(e) => {
				handleRename(e);
			}}
			width="full"
			fontSize='6xl'
			value={tag}
		>
			<Tooltip label={(user && user.userRole === 'ADMIN') ? 'Click to edit name' : ''}>
				<EditablePreview px={6} minW={'100%'} bgSize={'400px'} />
			</Tooltip>
			<Input type='text' as={EditableInput} onChange={e => { setTag(e.target.value); }} />
			<SaveControl />
		</Editable>}
		<AssetTable assets={assetsin} setSelectedAssets={setSelectedAssets} preSelIDs={[]} />
		{(user && user.userRole !== 'VIEWER') &&
			<ButtonGroup>
				<Button onClick={handleRemove}>Remove from tag</Button>
				<OperationTo actionFunc={handleCopy} actionName="Copy" />
				<OperationTo actionFunc={handleMove} actionName="Move" />
				{user.userRole === 'ADMIN' &&
					<Button colorScheme='red' variant={'solid'} onClick={handleDelete}>Delete Tag</Button>}
			</ButtonGroup>}
	</VStack>);
};

export default TagViewer;