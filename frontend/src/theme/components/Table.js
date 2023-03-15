import { tableAnatomy } from '@chakra-ui/anatomy';
import {createMultiStyleConfigHelpers } from '@chakra-ui/react';

const { definePartsStyle, defineMultiStyleConfig } =
  createMultiStyleConfigHelpers(tableAnatomy.keys);

const baseStyle = definePartsStyle({
	table: {
		mt:'4',
		borderWidth:'10px',
	  	width: '100%'
	}});
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
					bg:'white',
					color:'blue.900'
				}
			},
			'&:nth-of-type(even)': {
				td: {
					bg:'blue.100',
					color:'blue.900'
				}
			}
		}
	}
});


export const tableTheme = defineMultiStyleConfig({
	baseStyle,
	variants: {
		brand: brandPrimary,
	},
	defaultProps: {
		size: 'sm',
		variant: 'brand'
	  },
});