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
	Select,
} from '@chakra-ui/react';
import { Fragment } from 'react';
import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import FormField from '../components/FormField';
import data from './../api.json';
const AssetViewer = () => {
	const { id } = useParams();
	const [assetSate, setAssetState] = useState(null);
	const [isDisabled, setIsDisabled] = useState(false);
	const [tag, setTag] = useState('');
	const [startWithEditView, setStartWithEditView] = useState(true);
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
		console.log(assetSate);
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
		console.log(assetSate);
		console.log(tag);
		setAssetState((prevAssetState) => ({
			...prevAssetState,
			tags: [...prevAssetState.tags, tag],
		}));
		setTag('');
		console.log(assetSate);
	};
	const handleTagChange = (event) => {
		const value = event.target.value;
		setTag(value);
	};

	const [projects, setProjects] = useState(['General','LDAP services']);

	useEffect(() => {
		setAssetState(data[id]);
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
					startWithEditView={startWithEditView}
					onSubmitHandler={handleChange}
				/>
				<FormField
					fieldName="link"
					fieldType="url"
					fieldDefaultValue={assetSate.link}
					isDisabled={isDisabled}
					startWithEditView={startWithEditView}
					onSubmitHandler={handleChange}
				/>
				<FormField
					fieldName="type"
					fieldType="text"
					fieldDefaultValue={assetSate.type}
					isDisabled={isDisabled}
					startWithEditView={startWithEditView}
					onSubmitHandler={handleChange}
				/>
				<Select isDisabled={isDisabled} onChange={(e) => {
					handleChange('project', e.target.value);
				}}>
					{projects.map((value, key) => {
						return (<option key={key} value={value}>{value}</option>);})}
				</Select>
				<FormField
					fieldName="description"
					fieldType="text"
					fieldDefaultValue={assetSate.description}
					isDisabled={isDisabled}
					startWithEditView={startWithEditView}
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
								startWithEditView={startWithEditView}
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
