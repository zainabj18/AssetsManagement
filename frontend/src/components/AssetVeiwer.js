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
	Input,
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
const AssetViewer = ({ canEdit, isNew }) => {
	const { id } = useParams();
	const [assetSate, setAssetState] = useState(undefined);
	const [isDisabled, setIsDisabled] = useState(!canEdit);
	const [tag, setTag] = useState('');
	const [openEdit, setOpenEdit] = useState(isNew);
	const access_levels = ['PUBLIC', 'INTERNAL', 'RESTRICTED', 'CONFIDENTIAL'];
	const projects = ['General', 'LDAP services'];
	const type = {
		Framework: [
			{
				attribute_name: 'Programming language(s)',
				attribute_type: 'text',
				attribute_value: 'React,JS,CSS',
			},
			{
				attribute_name: 'no. of issues',
				attribute_type: 'number',
				attribute_value: 2,
			},
			{
				attribute_name: 'built On',
				attribute_type: 'datetime-local',
				attribute_value: '2021-12-10T13:45',
			},
			{
				attribute_name: 'version',
				attribute_type: 'text',
				attribute_value: 'v1',
			},
		],
		Document: [
			{
				attribute_name: 'draf',
				attribute_type: 'checkbox',
				attribute_value: false,
			},
			{
				attribute_name: 'version',
				attribute_type: 'text',
				attribute_value: 'v1',
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
		setAssetState((prevAssetState) => ({
			...prevAssetState,
			tags: [...prevAssetState.tags, tag],
		}));
		setTag('');
	};
	const handleTagChange = (event) => {
		const value = event.target.value;
		setTag(value);
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
		axios.post('http://127.0.0.1:5000/api/v1/asset/new', assetSate);
	};

	useEffect(() => {
		if (id) {
			const fetchData = async () => {
				const res = await axios.get('http://127.0.0.1:5000/api/v1/asset/' + id);
				console.log(res.data);
				return res;
			};
			fetchData().then((res)=>{setAssetState(res.data);}).catch((err) => {console.log(err);});

			setOpenEdit(false);
		} else {
			setAssetState({
				name: '',
				link: '',
				type: 'Framework',
				description: '',
				tags: [],
				project: '',
				access_level: 'PUBLIC',
				metadata: [],
			});
		}
	}, [id]);

	return assetSate ? (
		<Container>
			{assetSate && <VStack>
				<Heading size={'2xl'}>Asset Attributes</Heading>
				<StatGroup>
					<Stat>
						<StatLabel>Created At</StatLabel>
						<StatNumber>{assetSate.created_at}</StatNumber>
					</Stat>
					<Stat>
						<StatLabel>Last Modified</StatLabel>
						<StatNumber>{assetSate.last_modified_at}</StatNumber>
					</Stat>
				</StatGroup>
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
				<FormControl bg="white" color="black">
					<FormLabel>Type</FormLabel>
					<Select
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
				<FormControl bg="white" color="black">
					<FormLabel>Project</FormLabel>
					<Select
						isDisabled={isDisabled}
						onChange={(e) => {
							handleChange('project', e.target.value);
						}}
					>
						{projects.map((value, key) => {
							return (
								<option key={key} value={value}>
									{value}
								</option>
							);
						})}
					</Select>
				</FormControl>
				<FormControl bg="white" color="black">
					<FormLabel>Access Level</FormLabel>
					<Select
						isDisabled={isDisabled}
						onChange={(e) => {
							handleChange('access_level', e.target.value);
						}}
					>
						{access_levels.map((value, key) => {
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
				<Wrap spacing={4}>
					{assetSate.tags.map((value, key) => (
						<WrapItem key={key}>
							<Tag size={'md'} key={key}>
								<TagLabel>{value}</TagLabel>
								<TagCloseButton onClick={(e) => onTagClick(e, value)} />
							</Tag>
						</WrapItem>
					))}
					<Input
						placeholder="Enter Tag"
						value={tag}
						onChange={handleTagChange}
					/>
					<Button onClick={onNewTag}>Add Tag</Button>
				</Wrap>
				<Divider />
				<Heading size={'md'}>Type Attributes:</Heading>

				{assetSate.metadata.map((value, key) => {
					return (
						<Fragment key={key}>
							<FormField
								fieldName={value.attribute_name}
								fieldType={value.attribute_type}
								fieldDefaultValue={value.attribute_value}
								isDisabled={isDisabled}
								startWithEditView={openEdit}
								onSubmitHandler={handleMetadataChange}
							/>
						</Fragment>
					);
				})}
			</VStack>}
			<Button onClick={createNewAsset}>Sumbit</Button>
		</Container>
	) : null;
};

export default AssetViewer;
