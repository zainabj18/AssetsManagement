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
} from '@chakra-ui/react';
import { Fragment } from 'react';
import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import FormField from './FormField';
import axios from 'axios';
import { createTag, fetchAsset, fetchAssetClassifications, fetchProjects, fetchTags } from '../api';
import SearchSelect from './SearchSelect';
import ProjectSelect from './ProjectSelect';
import ListFormField from './ListFormField';
import SelectFormField from './SelectFormField';
import NumFormField from './NumFormField';
const AssetViewer = ({ canEdit, isNew }) => {
	const { id } = useParams();
	const [assetSate, setAssetState] = useState(undefined);
	const [isDisabled, setIsDisabled] = useState(!canEdit);
	const [tag, setTag] = useState('');
	const [openEdit, setOpenEdit] = useState(isNew);
	const [classifications,setClassifications] = useState([]);
	const [projects,setProjects] = useState([]);
	const [projectList,setProjectList]=useState([]);
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
				attribute_name: 'authors_emails',
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
		setAssetState((prevAssetState) => ({
			...prevAssetState,
			type: attribute_value,
			metadata: type[attribute_value],
		}));
	};

	const createNewAsset = (e) => {
		e.preventDefault();
		//axios.post('/api/v1/asset/new', assetSate);
		let project_ids=projects.map(p=>p.id);
		setAssetState((prevAssetState) => ({
			...prevAssetState,
			projects: project_ids,
		}));
		console.log(assetSate);
	};

	useEffect(() => {
		fetchAssetClassifications().then((data)=>{
			setClassifications(data.data);}).catch((err) => {console.log(err);});
		if (id) {
			fetchAsset(id).then((data)=>{
				setAssetState(data);}).catch((err) => {console.log(err);});
			setOpenEdit(false);
		} else {

			fetchProjects().then(
				(res)=>{
					console.log(res.data);
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
				access_level: 'PUBLIC',
				metadata: [],
			});
		}
	}, [id]);
	

	return assetSate ? (
		<Container>
			{assetSate && <VStack maxW='100%'>
				<Heading size={'2xl'}>Asset Attributes</Heading>
		
				<FormField
					fieldName="name"
					fieldType="text"
					fieldDefaultValue={assetSate.name}
					isDisabled={isDisabled}
					startWithEditView={openEdit}
					onSubmitHandler={handleChange}
				/>
				<FormField
					fieldName="link"
					fieldType="url"
					fieldDefaultValue={assetSate.link}
					isDisabled={isDisabled}
					startWithEditView={openEdit}
					onSubmitHandler={handleChange}
				/>
				<FormControl>
					<FormLabel>Type</FormLabel>
					<Select
						placeholder='Select a type'
						isDisabled={isDisabled || !isNew}
						onChange={(e) => {
							handleTypeChange(e, e.target.value);
						}}
					>
						{Object.keys(type).map((value, key) => {
							return (
								<option key={key} value={value}>
									{value}
								</option>
							);
						})}
					</Select>
				</FormControl>
				<FormControl>
					<FormLabel>Project</FormLabel>
					<Wrap spacing={4}>
						{projects.map((value, key) => (
							<WrapItem key={key}>
								<Tag size={'md'} key={key}>
									<TagLabel>{value.name}</TagLabel>
								</Tag>
							</WrapItem>
						))}
						<ProjectSelect setSelectedProjects={setProjects}  projects={projectList}/>
					</Wrap>
				</FormControl>
				<FormControl  >
					<FormLabel>Access Level</FormLabel>
					<Select
						isDisabled={isDisabled}
						onChange={(e) => {
							handleChange('access_level', e.target.value);
						}}
					>
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
					startWithEditView={openEdit}
					onSubmitHandler={handleChange}
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
								<ListFormField fieldName={value.attribute_name} fieldDefaultValue={value.attribute_value} validation={value.attribute_validation} onChangeHandler={handleMetadataChange}/>
							</Fragment>);
					case 'num_lmt':
						return (
							<Fragment key={key}> 
								<NumFormField fieldName={value.attribute_name} fieldDefaultValue={value.attribute_value} validation={value.attribute_validation}  onChangeHandler={handleMetadataChange}/>
							</Fragment>);
					case 'options':
						return (
							<Fragment key={key}> 
								<SelectFormField fieldName={value.attribute_name} fieldDefaultValue={value.attribute_value} validation={value.attribute_validation} onChangeHandler={handleMetadataChange}/>
							</Fragment>);
					default:
						return (<Fragment key={key}>
							<FormField
								fieldName={value.attribute_name}
								fieldType={value.attribute_type}
								fieldDefaultValue={value.attribute_value}
								isDisabled={isDisabled}
								startWithEditView={openEdit}
								onSubmitHandler={handleMetadataChange}
							/>
						</Fragment>);
					  }
				})}
			</VStack>}
			{!isNew && (<StatGroup>
				<Stat>
					<StatLabel>Created At</StatLabel>
					<StatNumber>{assetSate.created_at}</StatNumber>
				</Stat>
				<Stat>
					<StatLabel>Last Modified</StatLabel>
					<StatNumber>{assetSate.last_modified_at}</StatNumber>
				</Stat>
			</StatGroup>)}
			
			<Button onClick={createNewAsset} isDisabled={isDisabled} >Sumbit</Button>
		</Container>
	) : null;
};

export default AssetViewer;
