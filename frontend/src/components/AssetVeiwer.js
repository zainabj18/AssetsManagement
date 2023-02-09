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
	AlertIcon,
	AlertTitle,
	AlertDescription,
	UnorderedList,
	ListItem,
} from '@chakra-ui/react';
import { Fragment } from 'react';
import { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import FormField from './FormField';
import axios from 'axios';
import { createTag, fetchTypesList, fetchAsset, fetchAssetClassifications, fetchProjects, fetchTags, fetchType, createAsset } from '../api';
import SearchSelect from './SearchSelect';
import ProjectSelect from './ProjectSelect';
import ListFormField from './ListFormField';
import SelectFormField from './SelectFormField';
import NumFormField from './NumFormField';
import useAuth from '../hooks/useAuth';
const AssetViewer = () => {
	const { id } = useParams();
	const {user} = useAuth();
	let navigate = useNavigate();
	const [assetSate, setAssetState] = useState(undefined);
	const [isDisabled, setIsDisabled] = useState(false);
	const [tag, setTag] = useState('');
	const [classifications,setClassifications] = useState([]);
	const [projects,setProjects] = useState([]);
	const [projectList,setProjectList]=useState([]);
	const [errors,setErrors]=useState([]);
	const [errorCount,setErrorCount]=useState(0);
	const [trigger,setTrigger]=useBoolean();
	const [types,setTypes]=useState([]);
	
	const handleChange = (attribute_name, attribute_value) => {
		setAssetState((prevAssetState) => ({
			...prevAssetState,
			[attribute_name]: attribute_value,
		}));
	};

	const handleMetadataChange = (attributeName, attribute_value) => {
		console.log(attribute_value);
		let metadata = assetSate.metadata;
		let newMetadata = metadata.map((attribute) => {
			if (attribute.attributeName === attributeName) {
				return {
					...attribute,
					attribute_value: attribute_value,
				};
			} else {
				return attribute;
			}
		});
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
		fetchType(attribute_value).then(res=>{
			console.log(res);
			setAssetState((prevAssetState) => ({
				...prevAssetState,
				type: attribute_value,
				metadata:res.metadata,
			}));
			setTrigger.toggle();
			console.log(res);

		});
	
	};

	const createNewAsset = (e) => {
		e.preventDefault();
		//axios.post('/api/v1/asset/new', assetSate);
		
		console.log(Object.entries(assetSate));
		console.log(assetSate.name.length);
		setErrors([]);
		let errs=[];
		for (const [key, value] of Object.entries(assetSate)) {
			if(value.length===0 && key!=='projects'){
				errs.push(key+' is required');
			}
			
		}
		if (projects.length===0){
			errs.push('project(s) is required');
		}
		if (errs.length===0){
			console.log('Sending data');
			
			let project_ids=projects.map(p=>p.id);
			let tag_ids=assetSate.tags.map(t=>t.id);
			let assetObj={
				...assetSate,
				projects: project_ids,
				tags:tag_ids
			};
			console.log(assetObj);
			createAsset(assetObj).then(res=>console.log(res)).catch(err=>console.log(err));
		}else{
			setErrors(errs);
		}

		
		// naviagte back to assets
	};

	useEffect(() => {
		fetchAssetClassifications().then((data)=>{
			setClassifications(data.data);}).catch((err) => {console.log(err);});

		fetchTypesList().then((data)=>{
			setTypes(data.data);}).catch((err) => {console.log(err);});
		if (id) {
			fetchAsset(id).then((data)=>{
				setAssetState(data);}).catch((err) => {console.log(err);});
			if (user.userRole==='VIEWER'){
				setIsDisabled(true);
			}
		} else {
			if (user.userRole==='VIEWER'){
				navigate('/');
			}
			fetchProjects().then(
				(res)=>{
					setProjectList(res.data);
				}
			);
			setAssetState({
				name: '',
				link: '',
				type: '',
				description: '',
				tags: [],
				projects: [],
				classification: '',
				metadata: [],
			});
		}
	}, [id]);
	

	return assetSate ? (
		<Container>
			{assetSate && <VStack maxW='100%'>
				<Heading size={'2xl'}>Asset Attributes</Heading>
				{errors.length && <Alert status='error' flexDirection='column' alignItems='right'>
					<AlertIcon alignSelf='center'/>
					<AlertTitle>Invalid Form</AlertTitle>
					<AlertDescription ><UnorderedList>
						{errors.map((value, key)=><ListItem key={key}>{value}</ListItem>)}
					</UnorderedList></AlertDescription>
				</Alert>}
		
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
						isDisabled={isDisabled ||id}
						onChange={(e) => {
							handleTypeChange(e, e.target.value);
						}}
					>
						<option key={'placeholder'} selected disabled>
							Select a type
						</option>
						{
							types.map((value, key) => {
								return (
								
									<option key={key} value={value.type_id}>
										{value.type_name}
									</option>
								);
							})}
					</Select>
				</FormControl>
				<FormControl>
					<FormLabel>Projects</FormLabel>
					<Wrap spacing={4}>
						{projects.map((value, key) => (
							<WrapItem key={key}>
								<Tag size={'md'} key={key}>
									<TagLabel>{value.name}</TagLabel>
								</Tag>
							</WrapItem>
						))}
						{!isDisabled && <ProjectSelect setSelectedProjects={setProjects}  projects={projectList} />}
					</Wrap>
				</FormControl>
				<FormControl  >
					<FormLabel>classification</FormLabel>
					<Select
						isRequired
						isDisabled={isDisabled}
						onChange={(e) => {
							handleChange('classification', e.target.value);
						}}
					>
						<option key={'placeholder'} selected disabled>
							Select a classification
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
				/>
				<FormControl >
					<FormLabel>Tags</FormLabel>
					<Wrap spacing={4}>
						{assetSate.tags.map((value, key) => (
							<WrapItem key={key}>
								<Tag size={'md'} key={key}>
									<TagLabel>{value.name}</TagLabel>
									<TagCloseButton onClick={(e) => onTagClick(e, value)} />
								</Tag>
							</WrapItem>
						))}
						<SearchSelect dataFunc={fetchTags} selectedValue={tag} setSelectedValue={setTag} createFunc={createTag}/>
						{tag && <Button onClick={onNewTag} isDisabled={isDisabled}>Add Tag</Button>}
					</Wrap>
				</FormControl>

				<Divider />
				<Heading size={'md'}>Type Attributes:</Heading>
		

				{assetSate.metadata && assetSate.metadata.map((value, key) => {
					switch(value.attributeType) {
					case 'list':
						console.log('I am here');
						return (
							<Fragment key={key}> 
								<ListFormField fieldName={value.attributeName} fieldDefaultValue={value.attributeValue?value.attributeValue:[]} validation={value.validation} onChangeHandler={handleMetadataChange} setErrorCount={setErrorCount}/>
							</Fragment>);
					case 'num_lmt':
						return (
							<Fragment key={key}> 
								<NumFormField fieldName={value.attributeName} fieldDefaultValue={value.attributeValue?value.attributeValue:value.validation.min} validation={value.validation}  onChangeHandler={handleMetadataChange} setErrorCount={setErrorCount}/>
							</Fragment>);
					case 'options':
						return (
							<Fragment key={key}> 
								<SelectFormField fieldName={value.attributeName} fieldDefaultValue={value.attributeValue?value.attributeValue:[]} validation={value.validation} onChangeHandler={handleMetadataChange}/>
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
							/>
						</Fragment>);
					  }
				})}
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
			
			{!isDisabled && <Button onClick={createNewAsset}>Sumbit</Button>}
		</Container>
	) : null;
};

export default AssetViewer;
