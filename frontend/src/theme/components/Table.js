import { tableAnatomy } from '@chakra-ui/anatomy';
import {createMultiStyleConfigHelpers } from '@chakra-ui/react';

const { definePartsStyle, defineMultiStyleConfig } =
  createMultiStyleConfigHelpers(tableAnatomy.keys);

const brandPrimary = definePartsStyle({
	th: {
		border:'none'
	},
	thead:{
		tr:{
			bg:'blue.900',
			color:'blue.100'
		}
	},
	tbody:{
		tr: {
			border:'none',
			'&:nth-of-type(odd)': {
				td:{
					bg:'blue.200',
					color:'blue.900'
				}
			},
			'&:nth-of-type(even)': {
				td: {
					bg:'blue.900',
					color:'blue.100'
				}
			}
		}
	}
});


export const tableTheme = defineMultiStyleConfig({
	variants: {
		brand: brandPrimary,
	},
	defaultProps: {
		size: 'sm',
		variant: 'brand'
	  },
});