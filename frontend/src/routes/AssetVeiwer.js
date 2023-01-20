import { Container } from '@chakra-ui/react';
import FormField from '../components/FormField';

const AssetViewer = () => {
	const handleChange = (e) => {
		console.log(e);
	};

	return (
		<Container>
			<FormField
				fieldName="name"
				fieldType="text"
				fieldDefaultValue="name"
				isDisabled={false}
				startWithEditView={true}
				onSubmitHandler={handleChange}
			/>
		</Container>
	);
};

export default AssetViewer;
