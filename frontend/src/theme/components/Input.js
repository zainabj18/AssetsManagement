import { inputAnatomy } from '@chakra-ui/anatomy';
import { createMultiStyleConfigHelpers} from '@chakra-ui/react';
const { definePartsStyle, defineMultiStyleConfig } =
  createMultiStyleConfigHelpers(inputAnatomy.keys);

const brandPrimary = definePartsStyle({field: {
	bg:'blue.100',
	borderColor: 'red.900',
	borderSize:'lg',
	color:'blue.900',
	_placeholder: {
		color: 'blue.900',
	},
	_focusVisible:{
		boxShadow: 'highlight',
	},
}});


export const inputTheme = defineMultiStyleConfig({
	variants: {
		brand: brandPrimary,
	},
	defaultProps: {
		variant: 'brand'
	  },
});