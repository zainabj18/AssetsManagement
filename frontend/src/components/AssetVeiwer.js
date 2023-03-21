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
	Editable,
	EditablePreview,
	EditableInput,
} from '@chakra-ui/react';
import { Fragment } from 'react';
import { useEffect, useState } from 'react';
import { redirect, useNavigate, useParams } from 'react-router-dom';

import axios from 'axios';
import { createTag, fetchTypesList, fetchAsset, fetchAssetClassifications, fetchProjects, fetchTags, fetchType, createAsset, fetchAssetProjects, deleteAsset, updateAsset, fetchAssetLinks, fetchAssetSummary, fetchTypesNamesVersionList, fetchAssetUpgradeOptions } from '../api';
import ProjectSelect from './ProjectSelect';
import useAuth from '../hooks/useAuth';
import AssetSelect from './AssetSelect';
import NumFormField from './asset/formfields/NumFormField';
import FormField from './asset/formfields/FormField';
import SearchSelect from './asset/formfields/SearchSelect';
import SelectFormField from './asset/formfields/SelectFormField';
import ListFormField from './asset/formfields/ListFormField';

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
	
	const handleChange = (attribute_name, attribute_value) => {
		setAssetState((prevAssetState) => ({
			...prevAssetState,
			[attribute_name]: attribute_value,
		}));
	};

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
			console.log(res);
			setDependencies(res.dependsOn);
			setTrigger.toggle();

		});
	
	};
	const handleDelete = (e) => {
		deleteAsset(id);
		navigate('/assets');
	};

	const handleUpgrade = (e) => {
		console.log(upgradeData);
		let newMetadata=assetSate.metadata.filter((attribute) => !(attribute.attributeName in upgradeData[1]));
		console.log(newMetadata);
		newMetadata=[...newMetadata,...upgradeData[0]];
		console.log(newMetadata);
		setAssetState((prevAssetState) => ({
			...prevAssetState,
			version_id:upgradeData[2],
			metadata: newMetadata,
		}));
		setUpgradeable(false);
	};

	const createNewAsset = (e) => {
		e.preventDefault();
		//axios.post('/api/v1/asset/new', assetSate);
		console.log(Object.entries(assetSate));
		console.log(assetSate.name.length);
		setErrors([]);
		let errs=[];
		for (const [key, value] of Object.entries(assetSate)) {
			if(value.length===0 && key!=='projects' && key!=='assets'){
				errs.push(key+' is required');
			}
			
		}
		console.log(assetSate.metadata);
		for (const [key, value] of Object.entries(assetSate.metadata)){
			if(!value.validation.isOptional && (!(value.hasOwnProperty('attributeValue'))) || (value.hasOwnProperty('attributeValue') && value.attributeValue.length===0)){
				errs.push(value.attributeName);
			}
		}
	
		if (projects.length===0){
			errs.push('project(s) is required');
		}
		if (errs.length===0){
			console.log('Sending data');
			
			let project_ids=projects.map(p=>p.projectID);
			let tag_ids=assetSate.tags.map(t=>t.id);
			let asset_ids=assets.map(a=>assetsList[a].asset_id);
			let assetObj={
				asset_id:id,
				...assetSate,
				projects: project_ids,
				assets:asset_ids,
				tags:tag_ids
			};
			console.log(assetObj);
			if (id){
				updateAsset(id,assetObj).then(
					res=>fetchAsset(id).then((res)=>{
						setAssetState(res.data);}).catch(err=>{
						navigate('/assets');}
					)).catch(err=>console.log(err));

			}else{
				createAsset(assetObj).then(
				
					res=>navigate(`../${res.data}`)).catch(err=>console.log(err));
			}
			
		}else{
			setErrors(errs);
		}
		// naviagte back to assets
	};

	useEffect(() => {
		if (user===undefined){
			navigate('/');
		}
		fetchAssetClassifications().then((data)=>{
			setClassifications(data.data);}).catch((err) => {console.log(err);});

		fetchTypesNamesVersionList().then((data)=>{
			console.log(data,'I am types');
			setTypes(data.data);}).catch((err) => {console.log(err,'types eroro');});
		if (id) {
			fetchAsset(id).then((res)=>{
				console.log(res.data);
				setAssetState(res.data);}).catch(err=>{
				navigate('/assets');}
			);
			if (user.userRole==='VIEWER'){
				setIsDisabled(true);
			}
			fetchAssetProjects(id).then(
				(res)=>{
					console.log(res.data);
					setProjectList(res.data);
				}
			);
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
					console.log(preSelected,'pre selected');
					setAssets(preSelected);
				}
			);

			fetchAssetUpgradeOptions(id).then(
				(res)=>{
					setUpgradeable(res.canUpgrade);
					setUpgradeData(res.data);
					console.log(res.data);
				}
			);
		} else {
			if (!user||user.userRole==='VIEWER'){
				navigate('/assets');
			}
			fetchProjects().then(
				(res)=>{
					setProjectList(res.data);
				}
			);

			fetchAssetSummary().then(
				(res)=>{
			
					setAssetsList(res.data);

				}

			);
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
		<Box p={4} width={'60vw'} height={'80vh'} overflow="scroll">
			{assetSate && <VStack maxW='100%'>
				{errors.length && <Alert status='error' flexDirection='column' alignItems='right'>
					<AlertIcon alignSelf='center'/>
					<AlertTitle>Invalid Form</AlertTitle>
					<AlertDescription ><UnorderedList>
						{errors.map((value, key)=><ListItem key={key}>{value}</ListItem>)}
					</UnorderedList></AlertDescription>
				</Alert>}
				<VStack minW='100%' bg="white" color="blue.800" alignItems='left' 
					alignContent='left' p={6} borderRadius={6}>
					<Heading size={'2xl'} >Asset Attributes</Heading>
					<FormField
					//    border={'1px solid'}
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
							bg='white'
							isDisabled={isDisabled ||id}
							onChange={(e) => {
								handleTypeChange(e, e.target.value);
							}}
						>
							<option key={'placeholder'} selected disabled>
								{id?assetSate.type:'Select a type'}
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
								
								
								{upgradeData[1].length>0 && <Fragment>
									The following attributes will be removed:
									<UnorderedList>
										{upgradeData[1].map((value, key)=><ListItem key={key}>{value}</ListItem>)}
									</UnorderedList></Fragment>}
								{upgradeData[0].length>0 && <Fragment>
									The following attributes will be added:
									<UnorderedList>
										{upgradeData[0].map((value, key)=><ListItem key={key}>{value.attributeName}</ListItem>)}
									</UnorderedList></Fragment>}
							</AlertDescription>
						
							<Button onClick={handleUpgrade}>Upgrade</Button>
						</Alert>}
				
					</FormControl>
					<FormControl>
						<FormLabel>Projects</FormLabel>
						<Wrap spacing={4}>
							{projects.map((value, key) => (
								<WrapItem key={key}>
									<Tag key={key} variant='brand'>
										<TagLabel>{value.projectName}</TagLabel>
									</Tag>
								</WrapItem>
							))}
							{!isDisabled && <ProjectSelect setSelectedProjects={setProjects}  projects={projectList} />}
						</Wrap>
					</FormControl>
					<FormControl>
						<FormLabel>Related Assets</FormLabel>
						<Wrap spacing={4}>
							{assets.map((value, key) => (
								<WrapItem key={key}>
									<Tag key={key} variant='brand'>
										<TagLabel>{assetsList[value].name}</TagLabel>
									</Tag>
								</WrapItem>
							))}
							{!isDisabled &&   <AssetSelect setSelected={setAssets} assetsin={assetsList} />}
						</Wrap>
						{dependencies.length>0 && <Alert status='info' flexDirection='column' alignItems='right'>
							<AlertIcon alignSelf='left'/>
							<AlertTitle>The related assets must include assets of types: </AlertTitle>
							<AlertDescription ><UnorderedList>
								{dependencies.map((value, key)=><ListItem key={key}>{value.type_name}</ListItem>)}
							</UnorderedList></AlertDescription>
						</Alert>}
					</FormControl>

					
					<FormControl  >
						<FormLabel>classification</FormLabel>
						<Select
							isRequired
							bg='white'
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
				<VStack minW='100%' bg="white" color="blue.800"alignItems='left' marginY={5}
					alignContent='left' p={6} borderRadius={6}>
					<Heading size={'md'}>Type Attributes:</Heading>
		

					{assetSate.metadata && assetSate.metadata.map((value, key) => {
						switch(value.attributeType) {
						case 'list':
							console.log('I am here');
							return (
								<Fragment key={key}> 
									<ListFormField fieldName={value.attributeName} fieldDefaultValue={value.attributeValue?value.attributeValue:[]} validation={value.validation} onChangeHandler={handleMetadataChange} setErrorCount={setErrorCount} isDisabled={isDisabled}/>
								</Fragment>);
						case 'num_lmt':
							return (
								<Fragment key={key}> 
									<NumFormField fieldName={value.attributeName} fieldDefaultValue={value.attributeValue?value.attributeValue:value.validation.min} validation={value.validation}  onChangeHandler={handleMetadataChange} setErrorCount={setErrorCount} isDisabled={isDisabled}/>
								</Fragment>);
						case 'options':
							return (
								<Fragment key={key}> 
									<SelectFormField fieldName={value.attributeName} fieldDefaultValue={value.attributeValue?value.attributeValue:[]} validation={value.validation} onChangeHandler={handleMetadataChange} isDisabled={isDisabled}/>
								</Fragment>);
						default:
							return (<Fragment key={key}>
								<FormField
									fieldName={value.attributeName}
									fieldType={value.attributeType}
									fieldDefaultValue={value.attributeValue?value.attributeValue:''}
									isDisabled={isDisabled}
									onSubmitHandler={handleMetadataChange}
									trigger={trigger}
									setErrorCount={setErrorCount}
									validation={value.validation}
								/>
							</Fragment>);
					  }
					})}
				</VStack>
			</VStack>}
			
			{id && (<StatGroup>
				<Stat>
					<StatLabel>Created At</StatLabel>
					<StatNumber>{assetSate.created_at}</StatNumber>
				</Stat>
				<Stat>
					<StatLabel>Last Modified</StatLabel>
					<StatNumber>{assetSate.last_modified_at}</StatNumber>
				</Stat>
			</StatGroup>)}
			
			{!isDisabled  && <Button onClick={createNewAsset} marginY={5}>Sumbit</Button>}
			{id && !isDisabled && <Button onClick={handleDelete}>Delete</Button>}
		</Box>
	) : null;
};

export default AssetViewer;
