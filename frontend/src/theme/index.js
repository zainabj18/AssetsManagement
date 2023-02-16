// theme/index.js
import { extendTheme,withDefaultColorScheme } from '@chakra-ui/react';
import Link from './components/Link';
import FormLabel from './components/FormLabel';
import styles from './styles';
import { tagTheme } from './components/Tag';
import Button from './components/Button';
import { inputTheme } from './components/Input';
import shadows from './foundations/shadows';


const overrides = {
	styles,
	shadows:shadows,
	components: {
		Link,
		FormLabel,
		Button,
		Input:inputTheme,
		Tag:tagTheme
	}
};


export default extendTheme(overrides,withDefaultColorScheme({ colorScheme: 'blue' }));
