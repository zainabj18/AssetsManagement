// theme/index.js
import { extendTheme,withDefaultColorScheme } from '@chakra-ui/react';
import Link from './components/Link';
import FormLabel from './components/FormLabel';
import styles from './styles';
import { tagTheme } from './components/Tag';
import Button from './components/Button';

const overrides = {
	styles,
	components: {
		Link,
		FormLabel,
		Button,
		Tag:tagTheme
	}
};


export default extendTheme(overrides,withDefaultColorScheme({ colorScheme: 'blue' }));
