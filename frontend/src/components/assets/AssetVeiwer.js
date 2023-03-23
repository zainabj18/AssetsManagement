import {
	Container,
	Stat,
	StatLabel,
	StatNumber,
	StatGroup,
	Divider,
	VStack,
	Heading,
	Tag,
	TagLabel,
	TagCloseButton,
	Wrap,
	WrapItem,
	Button,
	FormControl,
	FormLabel,
	Select,
	useBoolean,
	Alert,
	Box,
	AlertIcon,
	AlertTitle,
	AlertDescription,
	UnorderedList,
	ListItem,
	useToast
} from '@chakra-ui/react';
import { Fragment } from 'react';
import { useEffect, useState } from 'react';
import { redirect, useNavigate, useParams } from 'react-router-dom';

import axios from 'axios';
import { createTag, fetchTypesList, fetchAsset, fetchAssetClassifications, fetchProjects, fetchTags, fetchType, createAsset, fetchAssetProjects, deleteAsset, updateAsset, fetchAssetLinks, fetchAssetSummary, fetchTypesNamesVersionList, fetchAssetUpgradeOptions } from '../../api';

import useAuth from '../../hooks/useAuth';
import AssetSelect from './AssetSelect';
import ProjectSelect from './ProjectSelect';
import NumFormField from './formfields/NumFormField';
import FormField from './formfields/FormField';
import SearchSelect from './formfields/SearchSelect';
import SelectFormField from './formfields/SelectFormField';
import ListFormField from './formfields/ListFormField';
import FormErrors from './FormErrors';
import MetadataFields from './MetadataFields';
import AssetsStats from './Stats';


const AssetViewer = () => {
	const { id } = useParams();
	const {user} = useAuth();
	let navigate = useNavigate();
	const [assetSate, setAssetState] = useState(undefined);
	const [isDisabled, setIsDisabled] = useState(false);
	const [tag, setTag] = useState('');
	const [classifications,setClassifications] = useState([]);
	const [projects,setProjects] = useState([]);
	const [assets,setAssets] = useState([]);
	const [assetsList,setAssetsList]=useState([]);
	const [projectList,setProjectList]=useState([]);
	const [dependencies,setDependencies]=useState([]);
	const [errors,setErrors]=useState([]);
	const [errorCount,setErrorCount]=useState(0);
	const [trigger,setTrigger]=useBoolean();
	const [types,setTypes]=useState([]);
	const [upgradeable,setUpgradeable]=useState(false);
	const [upgradeData,setUpgradeData]=useState(undefined);
	const toast = useToast();
	
	const handleChange = (attribute_name, attribute_value) => {
		setAssetState((prevAssetState) => ({
			...prevAssetState,
			[attribute_name]: attribute_value,
		}));
	};

	function addToast(description,err) {
		console.log(err);
		if (err.response) {
			if(err.response.status===400||err.response.status===422||err.response.status===500){
				let msg = err.response.data.msg;
				if (msg===undefined){
					msg=description;
				}
				toast({
					title: err.response.status+' '+ err.response.statusText,
					description: msg,
					status: 'warning',
					isClosable: true,
					duration: 9000,
					position:'bottom-left'
				});}
			else{
				toast({
					title: err.response.status+' '+ err.response.statusText,
					description: description,
					status: 'error',
					isClosable: true,
					position:'bottom-left'
				});}}
		else{
			toast({
				title: 'An error has occured',
				description: description,
				status: 'error',
				isClosable: true,
				position:'bottom-left'
			});

		}
		if (err.response.status===422){
			let errors=[];
			console.log(err.response.data.data);
			for (let i = 0; i < err.response.data.data.length; i++) {
				console.log(err.response.data);
				let name=Object.values(err.response.data.data[i]['loc'].toString());
				name=name.concat(' '+err.response.data.data[i]['msg']);
				errors.push(name);
			}
			console.log(errors);

			setErrors(errors);
		}
	}
	const handleMetadataChange = (attributeName, attribute_value) => {
		console.log(attribute_value);
		console.log('I am name');
		console.log(attributeName);
		let metadata = assetSate.metadata;
		let newMetadata = metadata.map((attribute) => {
			if (attribute.attributeName === attributeName) {
				return {
					...attribute,
					attributeValue: attribute_value,
				};
			} else {
				return attribute;
			}
		});
		console.log(newMetadata);
		setAssetState((prevAssetState) => ({
			...prevAssetState,
			metadata: newMetadata,
		}));
	};

	const onTagClick = (e, value) => {
		e.preventDefault();
		let newTags = assetSate.tags.filter((tag) => value !== tag);
		setAssetState((prevAssetState) => ({
			...prevAssetState,
			tags: newTags,
		}));
	};

	const onNewTag = (e) => {
		e.preventDefault();
		if (tag){
			console.log(assetSate);
			if (!assetSate.tags.some(t => Object.is(t, tag))){
				setAssetState((prevAssetState) => ({
					...prevAssetState,
					tags: [...prevAssetState.tags, tag],
				}));
			}
			setTag(null);
		}

	};

	const handleTypeChange = (e, attribute_value) => {
		e.preventDefault();
		console.log(attribute_value);
		fetchType(attribute_value).then(res=>{
			setAssetState((prevAssetState) => ({
				...prevAssetState,
				version_id: attribute_value,
				metadata:res.metadata,
			}));
			console.log('depednecnuezs');
			console.log(res);
			setDependencies(res.dependsOnNames);
			console.log(res.dependsOn);
			setTrigger.toggle();
		});
	
	};
	const handleDelete = (e) => {
		deleteAsset(id);
		navigate('/assets');
	};


	const handleUpgrade = (e) => {
		console.log(upgradeData);
		let newMetadata=assetSate.metadata.filter((attribute) => !(attribute.attributeName in upgradeData['removedAttributesNames']));
		console.log(newMetadata);
		newMetadata=[...newMetadata,...upgradeData['addedAttributes']];
		console.log(newMetadata);
		setAssetState((prevAssetState) => ({
			...prevAssetState,
			version_id:upgradeData['maxVersion'],
			metadata: newMetadata,
		}));
		setUpgradeable(false);
	};

	const createNewAsset = (e) => {
		e.preventDefault();
		console.log(assetSate);
		const REQUIRED_FIELDS=['name','link','version_id','description','classification'];
		setErrors([]);
		let errs=[];
		for (const field of REQUIRED_FIELDS){
			console.log(field);
			console.log(assetSate.hasOwnProperty(field));
			if ((!assetSate.hasOwnProperty(field)) ||  ((assetSate.hasOwnProperty(field)) && assetSate[field].length===0)){
				if (field==='version_id'){
					errs.push('type is required');
				}else{
					errs.push(field+' is required');

				}
				
			}
		}
		

		if (projects.length===0){
			errs.push('project(s) is required');
		}
		if (errs.length===0){
			console.log('Sending data');
			
			let projectIDs=projects.map(p=>projectList[p].projectID);
			let tagIDs=assetSate.tags.map(t=>t.id);
			let assetIDs=assets.map(a=>assetsList[a].assetID);
			let assetObj={
				assetID:id,
				...assetSate,
				projectIDs: projectIDs,
				assetIDs:assetIDs,
				tagIDs:tagIDs
			};
			console.log(assetObj);
			
			if (id){
				console.log(assetObj);
				updateAsset(id,assetObj).then(res=>
					console.log('re')
				).catch(err=>{
					console.log(err);
					addToast('Unable to create asset',err);
				}
				);

			}else{
				console.log('bye');
				createAsset(assetObj).then(

					res=>{
						console.log('hello');
						navigate(`../${res.data}`);}).catch((err) => {
					console.log('I gete here');
					addToast('Unable to create asset',err);});
			}
		}else{
			setErrors(errs);
		}
	};

	useEffect(() => {
		if (user===undefined){
			navigate('/');
		}
		fetchAssetClassifications().then((data)=>{
			setClassifications(data.data);}).catch((err) => {
			addToast('Unable to get classifications',err);});

		fetchTypesNamesVersionList().then((data)=>{
			console.log(data,'I am types');
			setTypes(data.data);}).catch((err) => {
			addToast('Unable to get types',err);});
		if (id) {
			fetchAsset(id).then((res)=>{
				setAssetState(res.data);});
			if (user.userRole==='VIEWER'){
				setIsDisabled(true);
			}
			fetchAssetProjects(id).then(
				(res)=>{
					let rowIDs=res.data.map((val,index)=>index);
					rowIDs =rowIDs.filter((rowID) => res.data[rowID].isSelected);
					setProjects(rowIDs);
					setProjectList(res.data);
				}
			).catch((err) => {
				toast({
					title: 'An error occurred.',
					description: 'Unable to get projects',
					status: 'error',
				});});
			fetchAssetLinks(id).then(
				(res)=>{
					console.log(res.data,'I am assets');
					setAssetsList(res.data);
					let preSelected=[];
					for (let i = 0; i < res.data.length; i++) {
						let obj=res.data[i];
						if (obj.hasOwnProperty('isSelected')&obj.isSelected){
							preSelected.push(i);
						}
					}

					setAssets(preSelected);
				}
			).catch((err) => {
				addToast('Unable to get asset links',err);});

			fetchAssetUpgradeOptions(id).then(
				(res)=>{
					setUpgradeable(!Array.isArray(res.data));
					setUpgradeData(res.data);
					console.log('I am upgrade');
					console.log(res.data);
				}
			).catch((err) => {
				addToast('Unable to get upgrade options',err);});
		} else {
			if (!user||user.userRole==='VIEWER'){
				navigate('/assets');
			}
			fetchProjects().then(
				(res)=>{
					setProjectList(res.data);
					
				}
			).catch((err) => {
				addToast('Unable to get projects',err);});

			fetchAssetSummary().then(
				(res)=>{
					setAssetsList(res.data);
				}
			).catch((err) => {
				addToast('Unable to get assets',err);});
			setAssetState({
				name: '',
				link: '',
				version_id: '',
				description: '',
				tags: [],
				projects: [],
				assets: [],
				classification: '',
				metadata: [],
			});
		}
		
	}, [id,user]);
	

	return assetSate ? (
		<Container p={4} maxW='100%'>
			{assetSate && <VStack maxW='100%'>
				<FormErrors errors={errors} />
				<VStack minW='100%' bg="white" color="blue.800" alignItems='left' 
					alignContent='left' p={6} borderRadius={6}>
					<Heading size={'2xl'} >Asset Attributes</Heading>
					<FormField
						fieldName="name"
						fieldType="text"
						fieldDefaultValue={assetSate.name}
						isDisabled={isDisabled}
						onSubmitHandler={handleChange}
						setErrorCount={setErrorCount}
					/>
					<FormField
						fieldName="link"
						fieldType="url"
						fieldDefaultValue={assetSate.link}
						isDisabled={isDisabled}
						onSubmitHandler={handleChange}
						setErrorCount={setErrorCount}
					/>
					<FormControl isRequired>
						<FormLabel>Type</FormLabel>
						<Select
							isRequired
							bg='blue.100'
							isDisabled={isDisabled ||id}
							onChange={(e) => {
								handleTypeChange(e, e.target.value);
							}}
						>
							<option key={'placeholder'} selected disabled>
								{id?assetSate.type_name:'Select a type'}
							</option>
							{
								types.map((value, key) => {
									return (
										<option key={key} value={value.version_id}>
											{value.type_name}
										</option>
									);
								})}
						</Select>
						{!isDisabled && upgradeable && <Alert status='warning' flexDirection='column' alignItems='right'>
							<AlertIcon alignSelf='center'/>
							<AlertTitle>It looks like a newer version of type is availiable.Please upgrade to the latest version.</AlertTitle>
							<AlertDescription>
								
								
								{upgradeData['removedAttributesNames'].length>0 && <Fragment>
									The following attributes will be removed:
									<UnorderedList>
										{upgradeData['removedAttributesNames'].map((value, key)=><ListItem key={key}>{value}</ListItem>)}
									</UnorderedList></Fragment>}
								{upgradeData['addedAttributes'].length>0 && <Fragment>
									The following attributes will be added:
									<UnorderedList>
										{upgradeData['addedAttributes'].map((value, key)=><ListItem key={key}>{value.attributeName}</ListItem>)}
									</UnorderedList></Fragment>}
								{upgradeData['dependsOn'].length>0 && <Fragment>
									The following dependencies are needed:
									<UnorderedList>
										{upgradeData['dependsOn'].map((value, key)=><ListItem key={key}>{value}</ListItem>)}
									</UnorderedList></Fragment>}
							</AlertDescription>
						
							<Button onClick={handleUpgrade}>Upgrade</Button>
						</Alert>}
				
					</FormControl>
					<FormControl>
						<FormLabel>Projects</FormLabel>
						{projectList.length>=projects.length && 
						<Wrap spacing={4}>
							{projects.map((value, key) => (
								<WrapItem key={key}>
									<Tag key={key} variant='brand'>
										{console.log(projectList[value].projectName)}
										<TagLabel>{projectList[value].projectName}</TagLabel>
									</Tag>
								</WrapItem>
							))}
							{!isDisabled && <ProjectSelect setProjectSelect={setProjects}  projectin={projectList} />}
						</Wrap>}
					</FormControl>
					<FormControl>
						<FormLabel>Related Assets</FormLabel>
						<Wrap spacing={4}>
							{assets.map((value, key) => (
				
								<WrapItem key={key}>
									{console.log(value)}
									{console.log(value.name)}
									<Tag key={key} variant='brand'>
										<TagLabel>{assetsList[value].name}</TagLabel>
									</Tag>
								</WrapItem>
							))}
							{!isDisabled &&   <AssetSelect setAssetSelected={setAssets} assetsin={assetsList} />}
						</Wrap>
						{dependencies.length>0 && <Alert status='info' flexDirection='column' alignItems='right'>
							<AlertIcon alignSelf='left'/>
							<AlertTitle>The related assets must include assets of types: </AlertTitle>
							<AlertDescription ><UnorderedList>
								{dependencies.map((value, key)=><ListItem key={key}>{value}</ListItem>)}
							</UnorderedList></AlertDescription>
						</Alert>}
					</FormControl>

					
					<FormControl  >
						<FormLabel>classification</FormLabel>
						<Select
							isRequired
							bg='blue.100'
							isDisabled={isDisabled}
							onChange={(e) => {
								handleChange('classification', e.target.value);
							}}
						>
							<option key={'placeholder'} selected disabled>
								{id?assetSate.classification:'Select a classification'}
							</option>
							{classifications.map((value, key) => {
								return (
									<option key={key} value={value}>
										{value}
									</option>
								);
							})}
						</Select>
					</FormControl>
					<FormField
						fieldName="description"
						fieldType="text"
						fieldDefaultValue={assetSate.description}
						isDisabled={isDisabled}
						onSubmitHandler={handleChange}
						setErrorCount={setErrorCount}
						isTextarea={true}
					/>
					<FormControl >
						<FormLabel>Tags</FormLabel>
						<Wrap spacing={4}>
							{assetSate.tags.map((value, key) => (
								<WrapItem key={key}>
									<Tag key={key}>
										<TagLabel>{value.name}</TagLabel>
										{(!isDisabled) && <TagCloseButton onClick={(e) => onTagClick(e, value)} />}
									</Tag>
								</WrapItem>
							))}
							{(tag ||!isDisabled) && (<>
								<SearchSelect dataFunc={fetchTags} selectedValue={tag} setSelectedValue={setTag} createFunc={createTag}/>
								<Button onClick={onNewTag} isDisabled={isDisabled}>Add Tag</Button></>)}
						</Wrap>
					</FormControl>
				</VStack>

				<Divider size='xl'/>
				<MetadataFields assetSate={assetSate} isDisabled={isDisabled} handleMetadataChange={handleMetadataChange} trigger={trigger} setErrorCount={setErrorCount}/>
			</VStack>}
			
			{id && (<AssetsStats created_at={assetSate.created_at} last_modified_at={assetSate.last_modified_at}/>
			
			)}
			
			{!isDisabled  && <Button onClick={createNewAsset}>Sumbit</Button>}
			{id && !isDisabled && <Button onClick={handleDelete}>Delete</Button>}
		</Container>
	) : null;
};

export default AssetViewer;
