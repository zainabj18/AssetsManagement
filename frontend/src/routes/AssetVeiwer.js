import {
	Container,
	Stat,
	StatLabel,
	StatNumber,
	StatGroup,
	Divider,
	VStack,
	Heading,
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
	const [startWithEditView, setStartWithEditView] = useState(true);
	const handleChange = (attributeName, attributeValue) => {
		setAssetState((prevAssetState) => ({
			...prevAssetState,
			[attributeName]: attributeValue,
		}));
	};

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
				<FormField
					fieldName="description"
					fieldType="text"
					fieldDefaultValue={assetSate.description}
					isDisabled={isDisabled}
					startWithEditView={startWithEditView}
					onSubmitHandler={handleChange}
				/>
				<FormField
					fieldName="ds"
					fieldType="checkbox"
					fieldDefaultValue={true}
					isDisabled={isDisabled}
					startWithEditView={startWithEditView}
					onSubmitHandler={handleChange}
				/>
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
								onSubmitHandler={handleChange}
							/>
						</Fragment>
					);
				})}
			</VStack>
		</Container>
	) : null;
};

export default AssetViewer;
