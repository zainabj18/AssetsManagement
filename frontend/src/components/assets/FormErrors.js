import { Alert, AlertDescription, AlertIcon, AlertTitle, ListItem, UnorderedList } from '@chakra-ui/react';

const FormErrors = ({errors}) => {
	return errors.length ? (<Alert status='error' flexDirection='column' alignItems='right'>
		<AlertIcon alignSelf='center'/>
		<AlertTitle>Invalid Form</AlertTitle>
		<AlertDescription ><UnorderedList>
			{errors.map((value, key)=><ListItem key={key}>{value}</ListItem>)}
		</UnorderedList></AlertDescription>
	</Alert>):null;};
	
export default FormErrors;