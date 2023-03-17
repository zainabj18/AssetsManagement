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
			bg:'#05386B',
			color:'white'
		}
	},
	tbody:{
		tr: {
			border:'none',
			'&:nth-of-type(odd)': {
				td:{
					bg:'#379683',
					color:'#05386B'
				}
			},
			'&:nth-of-type(even)': {
				td: {
					bg:'#EDF5E1',
					color:'#05386B'
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