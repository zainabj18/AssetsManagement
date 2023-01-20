import {
	Container,
	Stat,
	StatLabel,
	StatNumber,
	StatGroup,
} from '@chakra-ui/react';
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
		</Container>
	) : null;
};

export default AssetViewer;
