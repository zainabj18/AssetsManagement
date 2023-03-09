import { modalAnatomy as parts } from '@chakra-ui/anatomy';
import { createMultiStyleConfigHelpers } from '@chakra-ui/styled-system';

const { definePartsStyle, defineMultiStyleConfig } =
	createMultiStyleConfigHelpers(parts.keys);

const baseStyle = definePartsStyle({
	dialog: {
		bg: 'gray.500',
		color: 'blue.900'
	},
});


const popup = definePartsStyle({
	dialog: {
	  borderRadius: 'md',
	  bg: 'gray.300',
	  color: 'blue.900',
	},
});
  

export const modalTheme = defineMultiStyleConfig({
	baseStyle,
	variants: { popup }
});