import { Heading, VStack } from '@chakra-ui/react';
import { Fragment } from 'react';
import FormField from './formfields/FormField';
import ListFormField from './formfields/ListFormField';
import NumFormField from './formfields/NumFormField';
import SelectFormField from './formfields/SelectFormField';

const MetadataFields = ({assetSate,isDisabled,handleMetadataChange,trigger,setErrorCount}) => {
	return ( <VStack minW='100%' bg="gray.400" color="blue.800"alignItems='left' 
		alignContent='left' p={6} borderRadius={6}>
		<Heading size={'md'}>Type Attributes:</Heading>
		{assetSate.metadata && assetSate.metadata.map((value, key) => {
			switch(value.attributeType) {
			case 'list':
				console.log('I am here');
				return (
					<Fragment key={key}> 
						<ListFormField fieldName={value.attributeName} fieldDefaultValue={value.attributeValue?value.attributeValue:[]} validation={value.validation} onChangeHandler={handleMetadataChange} setErrorCount={setErrorCount} isDisabled={isDisabled}/>
					</Fragment>);
			case 'num_lmt':
				return (
					<Fragment key={key}> 
						<NumFormField fieldName={value.attributeName} fieldDefaultValue={value.attributeValue?value.attributeValue:value.validation.min} validation={value.validation}  onChangeHandler={handleMetadataChange} setErrorCount={setErrorCount} isDisabled={isDisabled}/>
					</Fragment>);
			case 'options':
				return (
					<Fragment key={key}> 
						<SelectFormField fieldName={value.attributeName} fieldDefaultValue={value.attributeValue?value.attributeValue:[]} validation={value.validation} onChangeHandler={handleMetadataChange} isDisabled={isDisabled}/>
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
						validation={value.validation}
					/>
				</Fragment>);
			}
		})}
	</VStack> );
};
 
export default MetadataFields;