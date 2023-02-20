import { Badge,Box } from '@chakra-ui/react';
import { useEffect, useMemo, useState } from 'react';
import { fetchAssetClassifications } from '../api';
import CustomTable from './CustomTable';

const AssetTable = ({assets,setSelectedAssets}) => {
	const [colours,setColors]=useState({});
	const columns =useMemo(()=>
	{ return {
		
		
		'asset_id':{
			header: 'Asset ID',
			canFilter:true	
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
	return (

		<CustomTable rows={assets} cols={columns}  setSelectedRows={setSelectedAssets}/>  );
};
 
export default AssetTable;