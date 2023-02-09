// theme/index.js
import { extendTheme,withDefaultColorScheme } from '@chakra-ui/react';
import Link from './components/Link';
import FormLabel from './components/FormLabel';
import styles from './styles';

const overrides = {
	styles,
	components: {
		Link,
		FormLabel,
		
	}
};


export default extendTheme(overrides,withDefaultColorScheme({ colorScheme: 'blue' }));
