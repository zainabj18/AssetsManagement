import {
	Box,
	Button,
	Center,
	Container,
	Divider,
	FormControl,
	FormLabel,
	Heading,
	Input,
	Select,
	Stat,
	StatGroup,
	StatLabel,
	StatNumber,
	Tab,
	TabList,
	TabPanel,
	TabPanels,
	Tabs,
	Tag,
	TagCloseButton,
	TagLabel,
	VStack,
	Wrap,
	WrapItem,
} from '@chakra-ui/react';
import axios from 'axios';
import { Fragment, useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import FormField from './FormField';
const RelatedAssetViewer = ({ canEdit, isNew }) => {
	const { id } = useParams();
	const [assetSate, setAssetState] = useState({
		name: 'name',
		link: 'link',
		description: 'description',
		tags: [],
		metadata: [],
		created_at: new Date().toUTCString(),
		last_modified_at: new Date().toUTCString(),
	});
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
		axios.post('/api/v1/asset/new', assetSate);
	};

	useEffect(() => {
		if (id) {
			const fetchData = async () => {
				const res = await axios.get('/api/v1/asset/get/' + id);
				console.log(res.data);
				return res;
			};
			fetchData()
				.then((res) => {
					setAssetState(res.data);
				})
				.catch((err) => {
					console.log(err);
				});

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
		<Center height={'100vh'}>
			<Box bg={'white'} color={'black'} p={10} borderRadius={10} w={'1000px'} mx={'auto'} mb={'100px'}>
				<Heading mb={'25px'}>View Asset</Heading>
				<Tabs>
					<TabList>
						<Tab>Attributes</Tab>
						<Tab>Types</Tab>
						<Tab>Projects</Tab>
						<Tab>Access Level</Tab>
						<Tab>Tags</Tab>
					</TabList>

					<TabPanels minH={300}>
						<TabPanel>
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
						</TabPanel>
						<TabPanel>
							<FormControl
								bg="white"
								color="black"
								borderRadius="5"
								border="3"
								borderColor="gray.200"
								padding={6}
							>
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
						</TabPanel>
						<TabPanel>
							<FormControl
								bg="white"
								color="black"
								borderRadius="5"
								border="3"
								borderColor="gray.200"
								padding={6}
							>
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
						</TabPanel>
						<TabPanel>
							<FormControl
								bg="white"
								color="black"
								borderRadius="5"
								border="3"
								borderColor="gray.200"
								padding={6}
							>
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
						</TabPanel>
						<TabPanel>
							<FormControl
								bg="white"
								color="black"
								borderRadius="5"
								border="3"
								borderColor="gray.200"
								padding={6}
							>
								<FormLabel>Tags</FormLabel>
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
							</FormControl>
						</TabPanel>
					</TabPanels>
				</Tabs>
				{!isNew && (
					<StatGroup m={'40px auto'}>
						<Stat>
							<StatLabel>Created At</StatLabel>
							<StatNumber>{assetSate.created_at}</StatNumber>
						</Stat>
						<Stat>
							<StatLabel>Last Modified</StatLabel>
							<StatNumber>{assetSate.last_modified_at}</StatNumber>
						</Stat>
					</StatGroup>
				)}

				<Button onClick={createNewAsset}>Sumbit</Button>
			</Box>
		</Center>
	) : null;
};

export default RelatedAssetViewer;
