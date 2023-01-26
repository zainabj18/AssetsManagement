// theme/index.js
import { extendTheme,withDefaultColorScheme } from '@chakra-ui/react';

import styles from './styles';


const overrides = {
	styles
};


export default extendTheme(overrides,withDefaultColorScheme({ colorScheme: 'blue' }));
