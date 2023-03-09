import { tagAnatomy } from '@chakra-ui/anatomy';
import { createMultiStyleConfigHelpers, defineStyle } from '@chakra-ui/react';

const { definePartsStyle, defineMultiStyleConfig } =
  createMultiStyleConfigHelpers(tagAnatomy.keys);

const brandPrimary = definePartsStyle({
	container: {
		bg: 'blue.300',
		fontWeight:'bold',
		border:'1px',
		borderRadius:10,
		borderColor:'blue.700',
		px: '4',
		py: '2',
	},
});


export const tagTheme = defineMultiStyleConfig({
	variants: {
		brand: brandPrimary,
	},
	defaultProps: {
		size: 'sm',
		variant: 'brand'
	  },
});