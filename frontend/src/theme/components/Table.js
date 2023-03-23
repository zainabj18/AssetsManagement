import { tableAnatomy } from '@chakra-ui/anatomy';
import {createMultiStyleConfigHelpers, position } from '@chakra-ui/react';

const { definePartsStyle, defineMultiStyleConfig } =
  createMultiStyleConfigHelpers(tableAnatomy.keys);

const baseStyle = definePartsStyle({
	table: {
		mt:'10',
		// borderWidth:'10px',
		maxHeight:'43vh',
	  	width: '100%'
	}});
const brandPrimary = definePartsStyle({
	th: {
		border:'none'
	},
	thead:{
		tr:{
			bg:'blue.900',
			color:'blue.100',
			position:'sticky',
			top:0
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
					bg:'blue.200',
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
	border:'none',
	defaultProps: {
		size: 'sm',
		variant: 'brand'
	  },
});