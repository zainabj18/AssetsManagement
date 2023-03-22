// theme/index.js
import { extendTheme,withDefaultColorScheme } from '@chakra-ui/react';
import Link from './components/Link';
import FormLabel from './components/FormLabel';
import styles from './styles';
import { tagTheme } from './components/Tag';
import Button from './components/Button';
import { modalTheme } from './components/Modal';
import { inputTheme } from './components/Input';
import shadows from './foundations/shadows';
import { tableTheme } from './components/Table';
import { checkboxTheme } from './components/Checkbox';


const overrides = {
	colors: {
		transparent: 'transparent',
		PUBLIC: 'green',
		INTERNAL: 'orange',
		RESTRICTED: 'brown',
		CONFIDENTIAL: 'red',
	},
	styles,
	shadows:shadows,
	components: {
		Link,
		FormLabel,
		Button,
		Checkbox:checkboxTheme,
		Modal:modalTheme,
		Input:inputTheme,
		Tag:tagTheme,
		Table:tableTheme,
	}
};


export default extendTheme(overrides,withDefaultColorScheme({ colorScheme: 'blue' }));
