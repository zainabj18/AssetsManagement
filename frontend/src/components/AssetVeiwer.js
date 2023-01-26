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
import data from '../api.json';
const AssetViewer = ({canEdit,isNew}) => {
	const { id } = useParams();
	const [assetSate, setAssetState] = useState(null);
	const [isDisabled, setIsDisabled] = useState(!canEdit);
	const [tag, setTag] = useState('');
	const [openEdit, setOpenEdit] = useState(isNew);
	const access_levels = ['PUBLIC', 'INTERNAL', 'RESTRICTED', 'CONFIDENTIAL'];
	const projects = ['General', 'LDAP services'];
	const type = {
		Framework: [
			{
				attributeName: 'trogramming tanguage(s)',
				attributeType: 'text',
				attributeValue: 'React,JS,CSS',
			},
			{
				attributeName: 'no. of issues',
				attributeType: 'number',
				attributeValue: 2,
			},
			{
				attributeName: 'built On',
				attributeType: 'datetime-local',
				attributeValue: '2021-12-10T13:45',
			},
			{
				attributeName: 'version',
				attributeType: 'text',
				attributeValue: 'v1',
			},
		],
		Document: [
			{
				attributeName: 'draf',
				attributeType: 'checkbox',
				attributeValue: false,
			},
			{
				attributeName: 'version',
				attributeType: 'text',
				attributeValue: 'v1',
			},
		],
	};
	const handleChange = (attributeName, attributeValue) => {
		setAssetState((prevAssetState) => ({
			...prevAssetState,
			[attributeName]: attributeValue,
		}));
	};

	const handleMetadataChange = (attributeName, attributeValue) => {
		let metadata = assetSate.metadata;
		let newMetadata = metadata.map((attribute) => {
			if (attribute.attributeName === attributeName) {
				return {
					...attribute,
					attributeValue: attributeValue,
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

	const handleTypeChange = (e,attributeValue) => {
		e.preventDefault();
		setAssetState((prevAssetState) => ({
			...prevAssetState,
			metadata: type[attributeValue],
		}));
	};

	useEffect(() => {
		if (id) {
			setAssetState(data[id]);
			setOpenEdit(false);
		} else {
			console.log('here');
			setAssetState({
				name: '',
				link: '',
				type: '',
				description: '',
				owner: '',
				tags: [],
				project: '',
				access_level: '',
				metadata:[]
			});		
		}
	}, [id]);

	return assetSate ? (
		<Container>
			<VStack>
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
						isDisabled={isDisabled||!isNew}
						onChange={(e) => {
							handleTypeChange(e,e.target.value);
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
						placeholder={assetSate.access_level ? assetSate.access_level:'PUBLIC'}
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
								fieldName={value.attributeName}
								fieldType={value.attributeType}
								fieldDefaultValue={value.attributeValue}
								isDisabled={isDisabled}
								startWithEditView={openEdit}
								onSubmitHandler={handleMetadataChange}
							/>
						</Fragment>
					);
				})}
			</VStack>
		</Container>
	) : null;
};

export default AssetViewer;
