import { modalAnatomy as parts } from '@chakra-ui/anatomy';
import { createMultiStyleConfigHelpers } from '@chakra-ui/styled-system';

const { definePartsStyle, defineMultiStyleConfig } =
	createMultiStyleConfigHelpers(parts.keys);

const baseStyle = definePartsStyle({
	dialog: {
		bg: 'white',
		color: 'black'
	},
});

export const modalTheme = defineMultiStyleConfig({
	baseStyle,
});