// theme/index.js
import { extendTheme,withDefaultColorScheme } from '@chakra-ui/react';
import Link from './components/Link';

import styles from './styles';


const overrides = {
	styles,
	components: {
		Link,
		
	}
};


export default extendTheme(overrides,withDefaultColorScheme({ colorScheme: 'blue' }));
