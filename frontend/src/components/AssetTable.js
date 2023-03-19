import { Badge,Box } from '@chakra-ui/react';
import { useEffect, useMemo, useState } from 'react';
import { Link as NavLink } from 'react-router-dom';
import { fetchAssetClassifications } from '../api';
import CustomTable from './CustomTable';
import {Link } from '@chakra-ui/react';
const AssetTable = ({assets,setSelectedAssets,preSelIDs,cols}) => {
	const [colours,setColors]=useState({});
	const columns =useMemo(()=>
	{ 
		console.log(cols);
		let orginal={
			'assetID':{
				header: 'Asset ID',
				canFilter:true,
				Cell:(rowID,value)=><Link to={`/assets/${value}`} as={NavLink}>{value}</Link>
			},
			'name':{
				header: 'Asset Name',
				canFilter:true
			},
			'type':{
				header: 'Asset Type',
				canFilter:true
			},
			'classification':{
				header: 'Asset Classification',
				canFilter:true,
				Cell:(rowID,value)=>{return <Badge bg={colours[value]} color={'white'}>{value}</Badge>;}
			},
		};
		if (cols){
			orginal={...orginal,...cols};
		}
		return orginal;
	}
	,[colours]);
	useEffect(() => {
		console.log(assets,'I am assets');
		fetchAssetClassifications().then((data)=>{
			let classification_levels=data.data;
			let customColours={};
			let RED=225;
			let GREEN=128;
			for (let i = 0; i < classification_levels.length; i++) {
				let factor=i/(classification_levels.length-1);
				customColours[classification_levels[i]]=`rgb(${factor*RED},${(1-factor)*GREEN},0)`;
			}
			console.log(customColours);
			setColors(customColours);
			
			
		}).catch((err) => {console.log(err);});},[]);
	return (colours && (

		<CustomTable rows={assets} cols={columns}  setSelectedRows={setSelectedAssets} preSelIDs={preSelIDs}/>  ));
};
 
export default AssetTable;