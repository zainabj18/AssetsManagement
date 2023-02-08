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
import { createTag, fetchTypesList, fetchAsset, fetchAssetClassifications, fetchProjects, fetchTags, fetchType } from '../api';
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
	const type = {
		Framework: [
			
			{
				attribute_name: 'no. of issues',
				attribute_type: 'number',
				attribute_value: 2,
			},
			{
				attribute_name: 'built on',
				attribute_type: 'datetime-local',
				attribute_value: '2021-12-10T13:45',
			},
			{
				attribute_name: 'version',
				attribute_type: 'text',
				attribute_value: 'v1',
			},
			{
				attribute_name: 'programming language(s)',
				attribute_type: 'options',
				attribute_value: ['React'],
				attribute_validation:{
					'values':['React','HTML','CSS','Python','Java'],
					'isMulti':true
				}
			},
			{
				attribute_name: 'license',
				attribute_type: 'options',
				attribute_value: 'MIT',
				attribute_validation:{
					'values':['MIT','GNU'],
					'isMulti':false
				}
			},
		],
		Document: [
			{
				attribute_name: 'draft',
				attribute_type: 'checkbox',
				attribute_value: false,
			},
			{
				attribute_name: 'version',
				attribute_type: 'text',
				attribute_value: 'v1',
			},
			{
				attribute_name: 'stars',
				attribute_type: 'num_lmt',
				attribute_value: 4,
				attribute_validation:{
					'min':1,
					'max':5
				}
			},
			{
				attribute_name: 'Authors Emails',
				attribute_type: 'list',
				attribute_value: ['mike@hotmail.com','carlos@hotmail.com','john@gmail.com'],
				attribute_validation:{
					'type':'email'
				}
			},
		],
	};
	const handleChange = (attribute_name, attribute_value) => {
		setAssetState((prevAssetState) => ({
			...prevAssetState,
			[attribute_name]: attribute_value,
		}));
	};

	const handleMetadataChange = (attribute_name, attribute_value) => {
		let metadata = assetSate.metadata;
		let newMetadata = metadata.map((attribute) => {
			if (attribute.attribute_name === attribute_name) {
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
		fetchType(attribute_value).then(res=>
			console.log(res.data)

		);
		let newMetadata=type[attribute_value];
		setAssetState((prevAssetState) => ({
			...prevAssetState,
			type: attribute_value,
			metadata:newMetadata,
		}));
		setTrigger.toggle();
	};

	const createNewAsset = (e) => {
		e.preventDefault();
		//axios.post('/api/v1/asset/new', assetSate);
		let project_ids=projects.map(p=>p.id);
		setAssetState((prevAssetState) => ({
			...prevAssetState,
			projects: project_ids,
		}));
		console.log(Object.entries(assetSate));
		console.log(assetSate.name.length);
		setErrors([]);
		for (const [key, value] of Object.entries(assetSate)) {
			if(value.length===0){
				setErrors((prev)=>[...prev,key+' is required']);
			}
		}
		console.log(errorCount);
		
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
				{errors && <Alert status='error' flexDirection='column' alignItems='right'>
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
		

				{assetSate.metadata.map((value, key) => {
					switch(value.attribute_type) {
					case 'list':
						console.log('I am here');
						return (
							<Fragment key={key}> 
								<ListFormField fieldName={value.attributeName} fieldDefaultValue={''} validation={value.validation} onChangeHandler={handleMetadataChange} setErrorCount={setErrorCount}/>
							</Fragment>);
					case 'num_lmt':
						return (
							<Fragment key={key}> 
								<NumFormField fieldName={value.attributeName} fieldDefaultValue={''} validation={value.validation}  onChangeHandler={handleMetadataChange} setErrorCount={setErrorCount}/>
							</Fragment>);
					case 'options':
						return (
							<Fragment key={key}> 
								<SelectFormField fieldName={value.attributeName} fieldDefaultValue={''} validation={value.validation} onChangeHandler={handleMetadataChange}/>
							</Fragment>);
					default:
						return (<Fragment key={key}>
							<FormField
								fieldName={value.attributeName}
								fieldType={value.attributeType}
								fieldDefaultValue={''}
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
